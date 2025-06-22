# newsbot

## Install

```
$ git clone https://github.com/yamamoto-tgz/newsbot.git
$ cd newsbot
$ pip install -r requirements.txt
```

## Environment Variables

| Name     | Required | Default |
| -------- | -------- | ------- |
| NB_PROXY | false    | None    |

## Example

```
$ flask --app newsbot.app run
$ flask --debug --app newsbot.app run
$ flask -e newsbot.env --app newsbot.app run
```
