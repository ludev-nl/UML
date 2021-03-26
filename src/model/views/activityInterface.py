from django.shortcuts import HttpResponse
from ..models import *
import os
import json
import uuid

class ActivityFrontendInterface():
    def __init__(self):
        self.nodes=dict()
        self.connections=dict()
        self.changes=dict()
        self.nodeTypes = ['initial','flowFinal','activityFinal','fork','merge','join','decision','action']

    def test1(self):
        ####    All in one activity
        ####
        ####    Initial -> Write name -> Read name -> Check name -> FinalNode
        ####
        a = Activity.objects.create(
            name='Test10'
        )
        i = InitialNode.objects.create(activity=a)
        aWrite = Action.objects.create(
            name='Write_name',
            description='Write name',
            activity=a
        )
        aRead = Action.objects.create(
            name='Read_name',
            description='Read name',
            activity=a
        )
        aCheck = Action.objects.create(
            name='Check_name',
            description='Check name',
            activity=a
        )
        f = ActivityFinalNode.objects.create(activity=a)
        e1 = ActivityEdge.objects.create(incoming_node=i, outgoing_node=aWrite, activity=a)
        e2 = ActivityEdge.objects.create(incoming_node=aWrite, outgoing_node=aRead, activity=a)
        e3 = ActivityEdge.objects.create(incoming_node=aRead, outgoing_node=aCheck, activity=a)
        e4 = ActivityEdge.objects.create(incoming_node=aCheck, outgoing_node=f, activity=a)
    
    def node(self, activityNode, node_type,node_id,node_activity_id):
        nodeInfo = ActivityNode.objects.get(id=node_id)
        return {
            'type': node_type,
            'name': str(nodeInfo.name),
            'data': {
                'description': nodeInfo.description,
                'activity_id': node_activity_id
            },
            'instances': {},
            'id': node_id
        }
    
    def connection(self, edge):
        return dict({
            str(uuid.uuid4()): {
                'guard': edge.guard,
                'weight': edge.weight,
                'from_id': str(edge.incoming_node_id),
                'to_id': str(edge.outgoing_node_id),
                'from': self.nodeUUID(
                    edge.incoming_node_id
                ),
                'to': self.nodeUUID(
                    edge.outgoing_node_id
                ),
                'id': edge.id
            }
        })
    
    def nodeUUID(self,node_id):
        for key, value in self.nodes.items():
            if value.get('id') == node_id:
                return key
        return ''

    def populateNodes(self):
        ''' Function to populate the different nodes.

        Creates a dictionary with all the types as key and the object set as value. Than for
        each of the object sets the nodes are added to the self.nodes
        '''
        #Activity nodes are not added. Should we add them? -> important for the zooming in.
        listOfNodes = {}

        listOfNodes['initial'] = InitialNode.objects.all()
        listOfNodes['flowFinal'] = FlowFinalNode.objects.all()
        listOfNodes['activityFinal'] = ActivityFinalNode.objects.all()
        listOfNodes['fork'] = ForkNode.objects.all()
        listOfNodes['merge'] = MergeNode.objects.all()
        listOfNodes['join'] = JoinNode.objects.all()
        listOfNodes['decision'] = DecisionNode.objects.all()
        listOfNodes['action'] = Action.objects.all()

        for key, value in listOfNodes.items():
            for node in value:
                nodeId = node.parentId()
                activityId = ActivityNode.objects.get(id=nodeId).activity_id
                self.nodes[str(uuid.uuid4())] = self.node(node,key,nodeId,activityId)


    def populateConnections(self):
        # implement control and objectflow
        for edge in ActivityEdge.objects.all():
            self.connections = {
                **self.connections,
                **self.connection(edge)
            }

    def request(self):
        self.populateNodes()
        self.populateConnections()
        print(self.nodes)
        print(self.connections)
        response = HttpResponse(str(json.dumps({
                'nodes': self.nodes,
                'connections': self.connections
            }))
        )
        response["Access-Control-Allow-Origin"] = "*"
        return response


    def delete(self, obj_type, pk):
        """Orchestration of the deletion of nodes and connections.

        Args:
            obj_type (str): the string representing a node or connection
            pk (str): primary key in the table
        """
        if obj_type == 'node':
            n = ActivityNode.objects.get(id=pk)
            n.delete()
        if obj_type == 'connection':
            edge = ActivityEdge.objects.get(id=pk)
            edge.delete()
    
    def newNode(self,obj_type,key,obj,activity_id):
        """Create a node for the defined node type.

        Args:
            obj_type (str): the type of node
            key (str): the key to the node
            obj (dict): information representing the object
        """
        #TODO
        activity = None
        if activity_id is None:
            return
        else:
            activity = Activity.objects.get(id=activity_id)

        if obj_type == 'initial':
            node = InitialNode.objects.create(activity=activity) 
        if obj_type == 'flowFinal':
            node = FlowFinalNode.objects.create(activity=activity)
        if obj_type == 'activityFinal':
            node = ActivityFinalNode.objects.create(activity=activity)
        if obj_type == 'fork':
            node = ForkNode.objects.create(activity=activity)
        if obj_type == 'merge':
            node = MergeNode.objects.create(activity=activity)
        if obj_type == 'join':
            node = JoinNode.objects.create(activity=activity)
        if obj_type == 'decision':
            node = DecisionNode.objects.create(activity=activity)
        if obj_type == 'action':
            node = Action.objects.create(
                name=obj.get('name'),
                description=obj.get('description'),
                activity=activity
            )
        print("nodeID: {}".format(node.id))
        self.nodes[key] = {'id': node.id}
    
    def newRelationship(self,key,obj,activity_id):
        """Create a relationship for the object.

        Args:
            obj (?): the object defining the relationship
        """
        node_from_id = self.nodes.get(obj.get('from')).get('id')
        node_from = ActivityNode.objects.get(id=node_from_id)

        node_to_id = self.nodes.get(obj.get('to')).get('id')
        node_to = ActivityNode.objects.get(id=node_to_id)

        activity = Activity.objects.get(id=activity_id)
        return ActivityEdge.objects.create(
            incoming_node=node_from,
            outgoing_node=node_to,
            activity=activity,
            guard=obj.get('guard'),
            weight=obj.get('weight')
        )
    
    def new(self, obj_type, key, obj):
        activity_id = obj.get('activity_id')
        if obj_type in self.nodeTypes:
            self.newNode(obj_type,key,obj,activity_id)
        if obj_type == 'connection':
            self.newRelationship(key,obj,activity_id)

    def retypeNode(self, obj_type, obj):
        """Retype certain properties of a node.

        Args:
            obj_type (str): type of object to be retyped
            obj (str): contains the data about the object
        """
        node = ActivityNode.objects.get(id=obj.get('id'))
        if obj.get('retype') == 'name':
            node.name = obj.get('name')
            node.save()
        if obj.get('retype') == 'description':
            node.description = obj.get('description')
            node.save()
    
    def retypeConnection(self, obj_type, obj):
        """Retype certain properties of a connection.

        Args:
            obj_type (str): type of object to be retyped
            obj (str): contains the data about the object
        """
        connection = ActivityEdge.objects.get(id=obj.get('id'))
        if obj.get('retype') == 'guard':
            connection.guard = obj.get('guard')
            connection.save()
        if obj.get('retype') == 'weight':
            connection.weight = obj.get('weight')
            connection.save()
        if obj.get('retype') == 'mirror':
            old_from = connection.incoming_node_id
            old_to = connection.outgoing_node_id
            connection.incoming_node_id = old_to
            connection.outgoing_node_id = old_from
            connection.save()

    def retype(self, obj_type, obj):
        """Retype certain properties of nodes and connections.

        Args:
            obj_type (str): type of object to be retyped
            obj (str): contains the data about the object
        """
        if obj_type == 'node':
            self.retypeNode(obj_type,obj)
        if obj_type == 'connection':
            self.retypeConnection(obj_type,obj)

    def push(self, request):
        """Push changes to the backend of the system.

        Args:
            request (?): request from the webpage
        """
        body = request.body.decode('utf-8')
        body_data = json.loads(body)

        self.changes = body_data.get('changes')
        self.nodes = body_data.get('nodes')
        self.connections = body_data.get('connections')

        for item in self.changes:
            action = item.get('type')
            if action.startswith('delete'):
                 self.delete(
                     action.split('-')[1],
                     item.get('key').get('id')
                )
            if action.startswith('new'):
                self.new(
                    action.split('-')[1],
                    item.get('key') or item.get('nodeKey'),
                    item.get('to')
                )
            if action.startswith('retype'):
                self.retype(
                    action.split('-')[1],
                    item.get('to')
                )
        return HttpResponse('OK')