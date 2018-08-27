#!/usr/bin/env python3.5

import sys
import Neo4jHandler
import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("configuration.ini")
    name = config.get("Neo4j", "Name")
    passw= config.get("Neo4j", "Password")
    connector = config.get("Neo4j", "Bolt")

    handler = Neo4jHandler.Neo4jHandler(uri=connector, user=name, password=passw)

    handler.execute_transaction(handler.remove_database_content)

    # Add host layer
    handler.execute_transaction(handler.add_host_layer_nodes)
    handler.execute_transaction(handler.add_host_layer_relationships)

    # Add system layer
    handler.execute_transaction(handler.add_system_layer_nodes)
    handler.execute_transaction(handler.add_system_layer_relationships)

    # Add network layer
    handler.execute_transaction(handler.add_network_layer_nodes)
    handler.execute_transaction(handler.add_network_layer_relationships)

    # Add detection and response layer
    handler.execute_transaction(handler.add_detection_and_response_layer_nodes)
    handler.execute_transaction(handler.add_detection_and_response_layer_relationships)

    # Add access control layer
    handler.execute_transaction(handler.add_access_control_layer_nodes)
    handler.execute_transaction(handler.add_access_control_layer_relationships)

    # Add mission layer
    handler.execute_transaction(handler.add_mission_layer_nodes)
    handler.execute_transaction(handler.add_mission_layer_relationships)

    # Add threath layer
    handler.execute_transaction(handler.add_threat_layer_nodes)
    handler.execute_transaction(handler.add_threat_layer_relationships)

    handler.close()
