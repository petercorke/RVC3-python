import IPython.kernel as kernel
# import ipykernel as kernel

# /Users/corkep/Library/Jupyter/runtime/kernel-5226.json
# Could not find 'kernel-5226.json' in ['.', '/Users/corkep/.ipython/profile_default/security']
# IPYTHONDIR/profile_<name>/security/kernel-<id>.json
# ipython kernel

cf = kernel.connect.find_connection_file('5571')
print(cf)

# https://stackoverflow.com/questions/9977446/connecting-to-a-remote-ipython-instance
# from IPython.zmq.blockingkernelmanager import BlockingKernelManager
# from IPython.kernel.blocking.client import BlockingKernelClient
from jupyter_client.blocking import BlockingKernelClient

client = BlockingKernelClient(connection_file=cf)
load connection info and init communication
client.load_connection_file()
client.start_channels()

def run_cell(km, code):
    # now we can run code.  This is done on the shell channel
    print()
    print("running:")
    print(code)

    # execution is immediate and async, returning a UUID
    msg_id = km.execute(code, silent=False)
    # msg_id = shell.send(code)
    # get_msg can block for a reply
    reply = km.get_shell_msg()

    status = reply['content']['status']
    if status == 'ok':
        print('succeeded!', reply['header']['msg_type'])
        print(reply['content'])
    elif status == 'error':
        print('failed!')
        for line in reply['content']['traceback']:
            print(line)

run_cell(client, 'a=5')
run_cell(client, 'print(7)')
run_cell(client, 'c=a/b')

# # msg_id = client.execute("print('hello')")
# msg_id = client.execute("1 + 10")

# # client.wait_for_ready()
# res = client.get_shell_msg(msg_id, timeout=1)
# print(res)
# print("----------------------------------------")
# msg = res["msg_id"]