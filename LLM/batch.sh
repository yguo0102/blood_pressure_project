set -x

#dataDir="datasets/ann_050724/"
#for k in 1 2 3 4 5;
#do
#	for model in meta-llama/Meta-Llama-3-70B-Instruct mistralai/Mixtral-8x7B-Instruct-v0.1;
#	do
#		name=$(basename -- "$model")
#		python run_offline_predict.py $model ${dataDir}/data_splits_${k}/test.csv ${dataDir}/data_splits_${k}/test.${name}.csv
#	done
#done


dataDir="datasets/ann_050724_new"
for model in meta-llama/Llama-2-7b-chat-hf /labs/sarkerlab/yguo262/LLM_open_source/finetuning/axolotl/lora_bp_pmc-out/HyperLlama meta-llama/Meta-Llama-3-70B-Instruct mistralai/Mixtral-8x7B-Instruct-v0.1;
do
	name=$(basename -- "$model")
	python run_offline_predict.py $model ${dataDir}/test.csv ${dataDir}/test.${name}.csv
done

