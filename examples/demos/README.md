# Running jupyter-notebook demos

Preconditions:
- python3 and pip3 are already installed
- your IP is on ACL whitelist. See: <https://portal.kentik.com/v4/settings/access>

Steps:
1. Open a new terminal

1. Set environment variables to your KentikAPI credentials  
`export KTAPI_AUTH_EMAIL=john.doe@acme.com`  
`export KTAPI_AUTH_TOKEN=__KentikAPIToken__`  

1. Install virtualenv - this allows you to create a python sandbox for your project  
`pip3 install virtualenv`

1. Create dedicated virtual environment  
`virtualenv .venv`

1. Activate virtualenv  
`source .venv/bin/activate`

1. Clone the library repository  
`git clone https://github.com/kentik/community_sdk_python.git`

1. `cd community_sdk_python/`

1. Install the library from repository  
`pip3 install -e kentik_api_library/`

1. Install demo requirements & jupyter-notebook
`pip3 install Pillow pandas httpretty notebook`

1. Run query result visualization demo  
`jupyter-notebook kentik_api_library/examples/demos/queries_visualisation_demo.ipynb`
