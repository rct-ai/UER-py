import torch
import argparse
import collections

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--input_model_path", type=str, default="google_model.bin",
                        help=".")
parser.add_argument("--output_model_path", type=str, default="huggingface_model.bin",
                        help=".")

args = parser.parse_args()
path = args.input_model_path

input_model = torch.load(args.input_model_path)

output_model = collections.OrderedDict()

output_model["bert.embeddings.word_embeddings.weight"] = input_model["embedding.word_embedding.weight"]
output_model["bert.embeddings.position_embeddings.weight"] = input_model["embedding.position_embedding.weight"]
output_model["bert.embeddings.token_type_embeddings.weight"] = input_model["embedding.segment_embedding.weight"][1:, :]
output_model["bert.embeddings.LayerNorm.weight"] = input_model["embedding.layer_norm.gamma"]
output_model["bert.embeddings.LayerNorm.bias"] = input_model["embedding.layer_norm.beta"]

for i in range(12):
    output_model["bert.encoder.layer." + str(i) + ".attention.self.query.weight"] = input_model["encoder.transformer." + str(i) + ".self_attn.linear_layers.0.weight"]
    output_model["bert.encoder.layer." + str(i) + ".attention.self.query.bias"] = input_model["encoder.transformer." + str(i) + ".self_attn.linear_layers.0.bias"]
    output_model["bert.encoder.layer." + str(i) + ".attention.self.key.weight"] = input_model["encoder.transformer." + str(i) + ".self_attn.linear_layers.1.weight"]
    output_model["bert.encoder.layer." + str(i) + ".attention.self.key.bias"] = input_model["encoder.transformer." + str(i) + ".self_attn.linear_layers.1.bias"]
    output_model["bert.encoder.layer." + str(i) + ".attention.self.value.weight"] = input_model["encoder.transformer." + str(i) + ".self_attn.linear_layers.2.weight"]
    output_model["bert.encoder.layer." + str(i) + ".attention.self.value.bias"] = input_model["encoder.transformer." + str(i) + ".self_attn.linear_layers.2.bias"]
    output_model["bert.encoder.layer." + str(i) + ".attention.output.dense.weight"] = input_model["encoder.transformer." + str(i) + ".self_attn.final_linear.weight"]
    output_model["bert.encoder.layer." + str(i) + ".attention.output.dense.bias"] = input_model["encoder.transformer." + str(i) + ".self_attn.final_linear.bias"]
    output_model["bert.encoder.layer." + str(i) + ".attention.output.LayerNorm.weight"] = input_model["encoder.transformer." + str(i) + ".layer_norm_1.gamma"]
    output_model["bert.encoder.layer." + str(i) + ".attention.output.LayerNorm.bias"] = input_model["encoder.transformer." + str(i) + ".layer_norm_1.beta"]
    output_model["bert.encoder.layer." + str(i) + ".intermediate.dense.weight"] = input_model["encoder.transformer." + str(i) + ".feed_forward.linear_1.weight"]
    output_model["bert.encoder.layer." + str(i) + ".intermediate.dense.bias"] = input_model["encoder.transformer." + str(i) + ".feed_forward.linear_1.bias"]
    output_model["bert.encoder.layer." + str(i) + ".output.dense.weight"] = input_model["encoder.transformer." + str(i) + ".feed_forward.linear_2.weight"]
    output_model["bert.encoder.layer." + str(i) + ".output.dense.bias"] = input_model["encoder.transformer." + str(i) + ".feed_forward.linear_2.bias"]
    output_model["bert.encoder.layer." + str(i) + ".output.LayerNorm.weight"] = input_model["encoder.transformer." + str(i) + ".layer_norm_2.gamma"]
    output_model["bert.encoder.layer." + str(i) + ".output.LayerNorm.bias"] = input_model["encoder.transformer." + str(i) + ".layer_norm_2.beta"]

output_model["bert.pooler.dense.weight"] = input_model["target.nsp_linear_1.weight"]
output_model["bert.pooler.dense.bias"] = input_model["target.nsp_linear_1.bias"]
output_model["cls.seq_relationship.weight"] = input_model["target.nsp_linear_2.weight"]
output_model["cls.seq_relationship.bias"] = input_model["target.nsp_linear_2.bias"]
output_model["cls.predictions.transform.dense.weight"] = input_model["target.mlm_linear_1.weight"]
output_model["cls.predictions.transform.dense.bias"] = input_model["target.mlm_linear_1.bias"]
output_model["cls.predictions.transform.LayerNorm.weight"] = input_model["target.layer_norm.gamma"]
output_model["cls.predictions.transform.LayerNorm.bias"] = input_model["target.layer_norm.beta"]
output_model["cls.predictions.decoder.weight"] = input_model["target.mlm_linear_2.weight"]
output_model["cls.predictions.bias"] = input_model["target.mlm_linear_2.bias"]

torch.save(output_model, args.output_model_path)