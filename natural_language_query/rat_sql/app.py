from flask import Flask, request, jsonify
from ratsql.commands import preprocess, train, infer, eval
import json
import _jsonnet
import attr

@attr.s
class PreprocessConfig:
    config = attr.ib()
    config_args = attr.ib()


@attr.s
class TrainConfig:
    config = attr.ib()
    config_args = attr.ib()
    logdir = attr.ib()


@attr.s
class InferConfig:
    config = attr.ib()
    config_args = attr.ib()
    logdir = attr.ib()
    section = attr.ib()
    beam_size = attr.ib()
    output = attr.ib()
    step = attr.ib()
    use_heuristic = attr.ib(default=False)
    mode = attr.ib(default="infer")
    limit = attr.ib(default=None)
    output_history = attr.ib(default=False)


@attr.s
class EvalConfig:
    config = attr.ib()
    config_args = attr.ib()
    logdir = attr.ib()
    section = attr.ib()
    inferred = attr.ib()
    output = attr.ib()

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    res_json = None
    model_config_args = None
    config_path = data.get('config_path')
    query_text = data.get('query_text')
    exp_config = json.loads(_jsonnet.evaluate_file(config_path))
    model_config_file = exp_config["model_config"]
    if "model_config_args" in exp_config:
        model_config_args = exp_config["model_config_args"]
    if model_config_args is not None:
        model_config_args_json = _jsonnet.evaluate_snippet("", args.model_config_args)
        model_config_args.update(json.loads(model_config_args_json))
        model_config_args = json.dumps(model_config_args)
    elif  model_config_args is not None:
        model_config_args = _jsonnet.evaluate_snippet("", args.model_config_args)
    else:
        model_config_args = None

    logdir = exp_config["logdir"]
    for step in exp_config["eval_steps"]:
                infer_output_path = f"{exp_config['eval_output']}/{exp_config['eval_name']}-step{step}.infer"
                infer_config = InferConfig(
                    model_config_file,
                    model_config_args,
                    logdir,
                    exp_config["eval_section"],
                    exp_config["eval_beam_size"],
                    infer_output_path,
                    step,
                    use_heuristic=exp_config["eval_use_heuristic"]
                )
                infer.main(infer_config)
                res_json = json.load(open(infer_output_path))
    return jsonify({'sql_result': res_json['all']})

if __name__ == '__main__':
    app.run()