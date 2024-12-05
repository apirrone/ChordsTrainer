# Chords Trainer

A python app that helps you train your chords on the piano (or any midi instrument actually).

## Installation

```bash
$ pip install -e .
```

## Usage

I'll add something to make it easier to select the relevant midi interface at some point. For now, you'll have to change the value in `__init__.py` :

```python
inport = mido.open_input(interfaces[1]) # This value (1)
```

Then run:

```bash
$ chords-trainer
```


## Message attributes
- msg.type
- msg.note
- msg.velocity
- msg.channel
