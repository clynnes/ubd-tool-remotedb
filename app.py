from flask import Flask, render_template 

from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

import os

app = Flask(__name__)
graph = Graph()

# getting the database reader endpoint as an environment variable
dbro = os.environ.get('NEPTUNEDBRO')

# Initial screen
@app.route('/')
def home():

    # initiate connection to graph
    remoteConn = DriverRemoteConnection(dbro,'g')
    g = graph.traversal().withRemote(remoteConn)

    # gets all the topics available in the database
    topics = g.V().hasLabel('application').values('topic').toSet()
    
    # close connection
    remoteConn.close()
    return render_template('init.html', topics=topics)

# About page
@app.route('/about')
def about():
    return render_template('about.html')



# Main screen 
@app.route('/<topic>/<app>') 
def main(topic, app): 

    # initiate graph connection
    remoteConn = DriverRemoteConnection(dbro,'g')
    g = graph.traversal().withRemote(remoteConn)

    # query for all topic property values and put into list
    topics = g.V().hasLabel('application').values('topic').toSet()
  
    # query only for application relating to specified topic
    relapps = g.V().has('application', 'topic', topic).elementMap().toList()
    
    
    # query for the first application in relapps list
    if(app == 'all'):
        appsel = None

        # query for datasets related to relapps[0]
        apps = g.V().has('application', 'topic', topic)
        datasets = apps.out().elementMap().toList()

    # query for single application (vertex) with name specified by parameter
    else:
        appsel = g.V().has('application', 'name', app).elementMap().toList()
        
        # query for all datasets relating to specified application
        selected = g.V().has('application', 'name', app)
        datasets = selected.out().elementMap().toList()
    
    # close connection
    remoteConn.close()
    return render_template('index.html', topic=topic, \
        topics=topics, apps=relapps, app=appsel, datasets=datasets)


if __name__ == '__main__':
    app.run(debug=True)




