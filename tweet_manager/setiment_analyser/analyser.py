from tokenizers import Tokenizer

import torch

PATH_TOKENIZER = '/home/chaudhary/projects/final_project_api_dev/tweet_manager/setiment_analyser/tokenizer.json'
PATH_MODEL = '/home/chaudhary/projects/final_project_api_dev/tweet_manager/setiment_analyser/model.pth'



#loading tokenizer
tokenizer = Tokenizer.from_file(PATH_TOKENIZER)



# handling two sentence and making the outpossible for bert
from tokenizers.processors import TemplateProcessing
tokenizer.post_processor = TemplateProcessing(
    single="[CLS] $A [SEP]",
    pair="[CLS] $A [SEP] $B:1 [SEP]:1",
    special_tokens=[
        ("[CLS]", tokenizer.token_to_id("[CLS]")),
        ("[SEP]", tokenizer.token_to_id("[SEP]")),
    ],
)

tokenizer.enable_padding(pad_id=tokenizer.token_to_id("[PAD]"), pad_token="[PAD]",length=100+2)
tokenizer.enable_truncation(max_length=100)




import math
import re
from random import *
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# BERT Parameters
maxlen = 102 # maximum of length
batch_size = 32
max_pred = 15  # max tokens of prediction
n_layers = 2 # number of Encoder of Encoder Layer
n_heads = 12 # number of heads in Multi-Head Attention
d_model = 768 # Embedding Size
d_ff = 768 * 4  # 4*d_model, FeedForward dimension
d_k = d_v = 64  # dimension of K(=Q), V
n_segments = 2
vocab_size = tokenizer.get_vocab_size()



def get_masked_token_pad_attention_mask(masked_tokens):
  batch_size, max_pred = masked_tokens.size()
  # eq(zero) is PAD token
  pad_attn_mask = masked_tokens.data.eq(tokenizer.token_to_id('[PAD]')) # [batch_size,max_pred] 
  pad_attn_mask = pad_attn_mask.view(batch_size,max_pred,1) # [batch_size,max_pred,1]

  pad_attn_mask = pad_attn_mask.expand(batch_size, max_pred,d_model) # [batch_size,max_pred,d_model]
  return pad_attn_mask


def get_attn_pad_mask(seq_q, seq_k):
    batch_size, len_q = seq_q.size()
    batch_size, len_k = seq_k.size()
    # eq(zero) is PAD token
    pad_attn_mask = seq_k.data.eq(tokenizer.token_to_id('[PAD]')).unsqueeze(1)  # batch_size x 1 x len_k(=len_q), one is masking
    return pad_attn_mask.expand(batch_size, len_q, len_k)  # batch_size x len_q x len_k

def gelu(x):
    "Implementation of the gelu activation function by Hugging Face"
    return x * 0.5 * (1.0 + torch.erf(x / math.sqrt(2.0)))

class Embedding(nn.Module):
    def __init__(self,vocab_size,d_model,maxlen,n_segments):
        super(Embedding, self).__init__()
        self.tok_embed = nn.Embedding(vocab_size, d_model)  # token embedding
        self.pos_embed = nn.Embedding(maxlen, d_model)  # position embedding
        self.seg_embed = nn.Embedding(n_segments, d_model)  # segment(token type) embedding
        self.norm = nn.LayerNorm(d_model)

    def forward(self, x, seg):
        seq_len = x.size(1)
        pos = torch.arange(seq_len, dtype=torch.long)
        pos = pos.unsqueeze(0).expand_as(x)  # (seq_len,) -> (batch_size, seq_len)
        embedding = self.tok_embed(x) + self.pos_embed(pos) + self.seg_embed(seg)
        return self.norm(embedding)


class ScaledDotProductAttention(nn.Module):
    def __init__(self):
        super(ScaledDotProductAttention, self).__init__()

    def forward(self, Q, K, V, attn_mask,d_k):
        scores = torch.matmul(Q, K.transpose(-1, -2)) / np.sqrt(d_k) # scores : [batch_size x n_heads x len_q(=len_k) x len_k(=len_q)]
        scores.masked_fill_(attn_mask, -1e9) # Fills elements of self tensor with value where mask is one.
        attn = nn.Softmax(dim=-1)(scores)
        context = torch.matmul(attn, V)
        return context, attn


class PoswiseFeedForwardNet(nn.Module):
    def __init__(self,d_model,d_ff):
        super(PoswiseFeedForwardNet, self).__init__()
        self.fc1 = nn.Linear(d_model, d_ff)
        self.fc2 = nn.Linear(d_ff, d_model)

    def forward(self, x):
        # (batch_size, len_seq, d_model) -> (batch_size, len_seq, d_ff) -> (batch_size, len_seq, d_model)
        return self.fc2(gelu(self.fc1(x)))


class MultiHeadAttention(nn.Module):
    def __init__(self,d_model,d_k,d_v,n_heads):
        super(MultiHeadAttention, self).__init__()
        self.W_Q = nn.Linear(d_model, d_k * n_heads)
        self.W_K = nn.Linear(d_model, d_k * n_heads)
        self.W_V = nn.Linear(d_model, d_v * n_heads)
    def forward(self, Q, K, V, attn_mask,n_heads,d_v,d_model,d_k):
        # q: [batch_size x len_q x d_model], k: [batch_size x len_k x d_model], v: [batch_size x len_k x d_model]
        residual, batch_size = Q, Q.size(0)
        # (B, S, D) -proj-> (B, S, D) -split-> (B, S, H, W) -trans-> (B, H, S, W)
        q_s = self.W_Q(Q).view(batch_size, -1, n_heads, d_k).transpose(1,2)  # q_s: [batch_size x n_heads x len_q x d_k]
        k_s = self.W_K(K).view(batch_size, -1, n_heads, d_k).transpose(1,2)  # k_s: [batch_size x n_heads x len_k x d_k]
        v_s = self.W_V(V).view(batch_size, -1, n_heads, d_v).transpose(1,2)  # v_s: [batch_size x n_heads x len_k x d_v]

        attn_mask = attn_mask.unsqueeze(1).repeat(1, n_heads, 1, 1) # attn_mask : [batch_size x n_heads x len_q x len_k]

        # context: [batch_size x n_heads x len_q x d_v], attn: [batch_size x n_heads x len_q(=len_k) x len_k(=len_q)]
        context, attn = ScaledDotProductAttention()(q_s, k_s, v_s, attn_mask,d_k=d_k)
        context = context.transpose(1, 2).contiguous().view(batch_size, -1, n_heads * d_v) # context: [batch_size x len_q x n_heads * d_v]
        output = nn.Linear(n_heads * d_v, d_model)(context)
        return nn.LayerNorm(d_model)(output + residual), attn # output: [batch_size x len_q x d_model]



class EncoderLayer(nn.Module):
    def __init__(self,d_model,d_k,d_v,n_heads,d_ff):
        super(EncoderLayer, self).__init__()
        self.enc_self_attn = MultiHeadAttention(d_model=d_model,d_k=d_k,d_v=d_v,n_heads=n_heads)
        self.pos_ffn = PoswiseFeedForwardNet(d_model=d_model,d_ff=d_ff)

    def forward(self, enc_inputs, enc_self_attn_mask):
        enc_outputs, attn = self.enc_self_attn(enc_inputs, enc_inputs, enc_inputs, enc_self_attn_mask,n_heads=n_heads,d_v=d_v,d_model=d_model,d_k=d_k) # enc_inputs to same Q,K,V
        enc_outputs = self.pos_ffn(enc_outputs) # enc_outputs: [batch_size x len_q x d_model]
        return enc_outputs, attn


class BERT(nn.Module):
    def __init__(self,d_model,n_layers,vocab_size,d_k,d_v,n_heads,d_ff):

        super(BERT, self).__init__()
        self.embedding = Embedding(vocab_size=vocab_size,d_model=d_model,maxlen=maxlen,n_segments=n_segments)
        self.layers = nn.ModuleList([EncoderLayer(d_model=d_model,d_k=d_k,d_v=d_v,n_heads=n_heads,d_ff=d_ff) for _ in range(n_layers)])
        self.fc = nn.Linear(d_model, d_model)
        self.activ1 = nn.Tanh()
        self.linear = nn.Linear(d_model, d_model)
        self.activ2 = gelu
        self.norm = nn.LayerNorm(d_model)
        self.classifier = nn.Linear(d_model, 2)
        # decoder is shared with embedding layer
        embed_weight = self.embedding.tok_embed.weight
        n_vocab, n_dim = embed_weight.size()
        self.decoder = nn.Linear(n_dim, n_vocab, bias=False)
        self.decoder.weight = embed_weight
        self.decoder_bias = nn.Parameter(torch.zeros(n_vocab))
        self.d_model = d_model

    def forward(self, input_ids, segment_ids, masked_pos,masked_tokens,max_pred):
        output = self.embedding(input_ids, segment_ids)
        enc_self_attn_mask = get_attn_pad_mask(input_ids, input_ids)
        for layer in self.layers:
            output, enc_self_attn = layer(output, enc_self_attn_mask)
        # output : [batch_size, len, d_model], attn : [batch_size, n_heads, d_model, d_model]
        # it will be decided by first token(CLS)
        h_pooled = self.activ1(self.fc(output[:, 0])) # [batch_size, d_model]
        logits_clsf = self.classifier(h_pooled) # [batch_size, 2]
        # get masked position from final output of transformer.
        h_masked = torch.ones(output.shape[0],max_pred,d_model) # [batch_size, max_pred, d_model]
        for i in range(output.shape[0]):
          h_masked[i] = torch.index_select(output[i],0,masked_pos[i])
        
        attention_mask = get_masked_token_pad_attention_mask(masked_tokens=masked_tokens)

        h_masked.masked_fill_(attention_mask,-1e9)
        h_masked_without_padding_info = nn.Softmax(dim=-1)(h_masked)
        h_masked = self.norm(self.activ2(self.linear(h_masked_without_padding_info)))
        logits_lm = self.decoder(h_masked) + self.decoder_bias # [batch_size, max_pred, n_vocab]

        return logits_lm, logits_clsf


class PoolingLayer(nn.Module):
    
    def __init__(self,model):
        super(PoolingLayer,self).__init__()
        self.model = model

    def forward(self, input_ids, segment_ids):
        output = self.model.embedding(input_ids, segment_ids)
        enc_self_attn_mask = get_attn_pad_mask(input_ids, input_ids)
        for layer in self.model.layers:
            output, enc_self_attn = layer(output, enc_self_attn_mask)
        # output : [batch_size, len, d_model], attn : [batch_size, n_heads, d_mode, d_model]
        # it will be decided by first token(CLS)
        h_pooled = self.model.activ1(self.model.fc(output[:, 0])) # [batch_size, d_model]

        return h_pooled


class FullyConnectedLayers(nn.Module):

  def __init__(self):
    super(FullyConnectedLayers,self).__init__()

    self.d1 = nn.Dropout(.75)
    self.d2 = nn.Dropout(.75)
    self.l1 = nn.Linear(768,2)
    # self.l2 = nn.Linear(100,2)
    # self.gelu = gelu

  def forward(self,h_pooled):

    fully_connected_layer_1 = self.l1(self.d1(h_pooled))

    # fully_connnected_layer_2 = gelu(self.l2(self.d2(fully_connected_layer_1)))


    # return fully_connnected_layer_2 
    return fully_connected_layer_1

class FineTurningBERT(nn.Module):

  def __init__(self,model):
    super(FineTurningBERT,self).__init__()

    self.pooling_layer = PoolingLayer(model)
    self.fully_connected_layers = FullyConnectedLayers()

  def forward(self,input_ids,segment_ids):

    pooled_output = self.pooling_layer(input_ids,segment_ids)

    out = self.fully_connected_layers(pooled_output)

    return out


checkpoint = torch.load(PATH_MODEL)
model = checkpoint['model']
model.eval()

import re
 
# https://catriscode.com/2021/05/01/tweets-cleaning-with-python/
def clean_tweet(tweet):
    temp = tweet.lower()
    # temp = re.sub("'", "", temp) # to avoid removing contractions in english
    # Removing hashtags and mentions
    temp = re.sub("@[A-Za-z0-9_]+","", temp)
    temp = re.sub("#[A-Za-z0-9_]+","", temp)
    # Removing links
    temp = re.sub(r'http\S+', '', temp)
    # Removing punctuations
    # temp = re.sub('[()!?]', ' ', temp)
    # temp = re.sub('\[.*?\]',' ', temp)
    temp = re.sub("[^a-z0-9]"," ", temp)

    return temp
def analyse(text):

    # encoding the text and converting to tokens
    with torch.no_grad():

        text_clean = clean_tweet(text)
        encoding = tokenizer.encode(text_clean)

        token_ids = encoding.ids
        segment_ids = encoding.type_ids

        token_ids = torch.tensor(token_ids).view(-1,102)
        
        segment_ids = torch.tensor(segment_ids)

        logits_clsf = model(token_ids,segment_ids)

        # print(logits_clsf)

        logits_clsf = logits_clsf.data.max(1)[1].data.flatten().item()

        # print(logits_clsf)
        return logits_clsf

analyse("have a safe journey")
