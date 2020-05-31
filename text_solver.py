from allennlp.predictors.predictor import Predictor as AllenNLPPredictor


class TextPredictor:
    def __init__(self):
        self.predictor = AllenNLPPredictor.from_path(
            "https://storage.googleapis.com/allennlp-public-models/bidaf-model-2020.02.10-charpad.tar.gz"
        )

    def predict(self, payload):
        prediction = self.predictor.predict(
            passage=payload["passage"], question=payload["question"]
        )
        return prediction["best_span_str"]


if __name__ == '__main__':
    predictor = TextPredictor()
    d = {'passage': 'If, in some cataclysm, all of scientific knowledge were to be destroyed, and only one sentence '
                    'passed on to the next generations of creatures, what statement would contain the most information '
                    'in the fewest words? I believe it is the atomic hypothesis (or the atomic fact, or whatever you '
                    'wish to call it) that all things are made of atoms—little particles that move around in perpetual '
                    'motion, attracting each other when they are a little distance apart, but repelling upon being '
                    'squeezed into one another. In that one sentence, you will see, there is an enormous amount of '
                    'information about the world, if just a little imagination and thinking are applied.',
         'question': 'what are atoms?'
         }
    print(predictor.predict(d))
