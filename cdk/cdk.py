from aws_cdk import App, Environment

from doctrina_build import DoctrinaBuildStack

app = App()
env = Environment()

humus_build = DoctrinaBuildStack(app, 'DoctrinaBuild', env=env)

app.synth()