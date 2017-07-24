How to run :

A. Test for bot running

- Connect with bot with http://t.me/FlagshipTestBot/ (need Telegram)
- Run bot with below code.
```sh
$ python3 MainRealTime.py
```
- Enter some chat and see feedback.
- Termination can be called through '/quit' on chat. If program is terminated without calling '/quit', last message might left on buffer on Telegram Server.

B. Test for stack structure
```sh
$ python3 MainStack.py
```
- During query input, some texts (coffee_service, set_field, recommend, print, stack, back, front) are used as commands.

Other note :

Currently, "field-set alert message" is unimplemented.
User should send one message to use this program. (Because sender id cannot obtained before message receiving...)