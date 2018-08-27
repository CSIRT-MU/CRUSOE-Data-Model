from neo4j.v1 import GraphDatabase, ServiceUnavailable
from neo4j.exceptions import AuthError
import sys


class Neo4jHandler(object):

    def __init__(self, uri, user, password):
        try:
            self._driver = GraphDatabase.driver(uri, auth=(user, password))
        except ServiceUnavailable:
            print("Can't connect to database, did  neo4j started ?")
            sys.exit()
        except AuthError:
            print("Client is unauthorized, check if your credentials are valid")
            sys.exit()

    def close(self):
        self._driver.close()

    # def execute_transaction(self):
    #     with self._driver.session() as session:
    #         transaction = session.write_transaction(self.remove_database_content)
    #         print(transaction)

    def execute_transaction(self, runnedmethod):
        with self._driver.session() as session:
            with session.begin_transaction() as tx:
                tx.run(runnedmethod())

    @staticmethod
    def remove_database_content():
        return "MATCH(n) OPTIONAL MATCH(n)-[m]-() DELETE n, m"

    @staticmethod
    def add_host_layer_nodes():
        return "LOAD CSV WITH HEADERS FROM \"file:///HostLayerNodes.csv\" AS csvline " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.VirtualHost) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Host:VirtualHost:Node {name:csvline.VirtualHost})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.PhysicalHost) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Host:PhysicalHost:Node {name:csvline.PhysicalHost})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Email) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Contact:Email {mail:csvline.Email})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Telephone) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Contact:Telephone {telephoneNumber:csvline.Telephone})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Cluster) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:HostCluster {clusterName:csvline.Cluster})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.SoftwareResource) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:SoftwareResource {name:csvline.SoftwareResource})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.NRPort) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:NetworkService {protocol:csvline.NRProtocol, port:csvline.NRPort}))"

    @staticmethod
    def add_host_layer_relationships():
        return "LOAD CSV WITH HEADERS FROM \"file:///HostLayerRelationships.csv\" AS csvline " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.HostedOn) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (virtual:VirtualHost {name:csvline.VirtualHost}) " \
               "MERGE (physical:PhysicalHost {name:csvline.HostedOn}) " \
               "CREATE (virtual)-[:hostedOn]->(physical)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Host) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (contMail:Email {mail:csvline.HasEmail}) " \
               "MERGE (contTelephone:Telephone {telephoneNumber:csvline.HasTelephone}) " \
               "MERGE (hos:Host {name:csvline.Host}) " \
               "CREATE (hos)-[:hasContact]->(contMail), (hos)-[:hasContact]->(contTelephone)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Host2) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (hos:Host {name:csvline.Host2}) " \
               "MERGE (cluster:HostCluster {clusterName:csvline.OnCluster}) " \
               "CREATE (hos)-[:partOf]->(cluster)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Host3) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (hos:Host {name:csvline.Host3}) " \
               "MERGE (cluster:HostCluster {clusterName:csvline.EntryPoint}) " \
               "CREATE (hos)-[:entryPoint]->(cluster)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Host4) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (hos:Host {name:csvline.Host4}) " \
               "MERGE (soft:SoftwareResource {name:csvline.SrrunsOn}) " \
               "CREATE (soft)-[:on {start:csvline.Start, end:csvline.End}]->(hos)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Cluster) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (clu:HostCluster {clusterName:csvline.Cluster}) " \
               "MERGE (soft:SoftwareResource {name:csvline.RunsOnCluster}) " \
               "CREATE (soft)-[:on {start:csvline.StartC, end:csvline.EndC}]->(clu)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.SoftwareResource) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (soft:SoftwareResource {name:csvline.SoftwareResource}) " \
               "MERGE (netw:NetworkService {port:csvline.NrprovidedPort}) " \
               "CREATE (soft)-[:provides]->(netw))"

    @staticmethod
    def add_system_layer_nodes():
        return "LOAD CSV WITH HEADERS FROM \"file:///SystemLayerNodes.csv\" AS csvline " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Component) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Component {name:csvline.Component})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Redundancy) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:RedundancyNode {name:csvline.Redundancy})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Dependency) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:DependencyNode {name:csvline.Dependency, Type:csvline.DependencyType})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Data) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Data {data:csvline.Data}))"

    @staticmethod
    def add_system_layer_relationships():
        return "LOAD CSV WITH HEADERS FROM \"file:///SystemLayerRelationships.csv\" AS csvline " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Component) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (comp:Component {name:csvline.Component}) " \
               "MERGE (depen:DependencyNode {name:csvline.DependsOn}) " \
               "CREATE (comp)-[:dependsOn]->(depen)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.DependencyNode) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (depen:DependencyNode {name:csvline.DependencyNode}) " \
               "MERGE (comp:Component {name:csvline.DependsComponent}) " \
               "CREATE (depen)-[:dependency]->(comp)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Redundancy) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (redund:RedundancyNode {name:csvline.Redundancy}) " \
               "MERGE (comp:Component {name:csvline.Component2}) " \
               "CREATE (comp)-[:providedBy]->(redund)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Component3) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (comp:Component {name:csvline.Component3}) " \
               "MERGE (dat:Data {data:csvline.Datas}) " \
               "CREATE (dat)-[:presentOn]->(comp)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.RedundancyNode) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (redu:RedundancyNode {name:csvline.RedundancyNode}) " \
               "MERGE (soft:SoftwareResource {name:csvline.SoftwareResource}) " \
               "CREATE (redu)-[:primaryInstance]->(soft)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Redundancy2) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (redu:RedundancyNode {name:csvline.Redundancy2}) " \
               "MERGE (soft:SoftwareResource {name:csvline.Software2}) " \
               "CREATE (redu)-[:redundancy]->(soft))"

    @staticmethod
    def add_network_layer_nodes():
        return "LOAD CSV WITH HEADERS FROM \"file:///NetworkLayerNodes.csv\" AS csvline " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Node) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Node {name:csvline.Node, " \
               "routingRules:csvline.Routerrule, filteringRules:csvline.FilterRule})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.IP) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:IP {ipAddress:csvline.IP})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.DomainName) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:DomainName {name:csvline.DomainName})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Subnet) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Subnet {subnet:csvline.Subnet, vlan:csvline.SubnetVlan," \
               " contact:csvline.SubnetContact, range:csvline.SubnetRange}))"

    @staticmethod
    def add_network_layer_relationships():
        return "LOAD CSV WITH HEADERS FROM \"file:///NetworkLayerRelationships.csv\" AS csvline " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.NodeHost) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (node:Node {name:csvline.NodeHost}) " \
               "MERGE (ip:IP {ipAddress:csvline.IPHost}) " \
               "CREATE (node)-[:hasAssigned {start:csvline.StartHost, end:csvline.EndHost}]->(ip)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Node) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (node:Node {name:csvline.Node}) " \
               "MERGE (ip:IP {ipAddress:csvline.IP2}) " \
               "CREATE (node)-[:hasAssigned {start:csvline.Start, end:csvline.End}]->(ip)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Ippart) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (subnet:Subnet {subnet:csvline.SubnetPart}) " \
               "MERGE (ip:IP {ipAddress:csvline.Ippart}) " \
               "CREATE (ip)-[:partOf]->(subnet)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.SubnetpartSubnet) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (subnet:Subnet {subnet:csvline.SubnetpartSubnet}) " \
               "MERGE (subnet2:Subnet {subnet:csvline.BigSubnet}) " \
               "CREATE (subnet)-[:partOf]->(subnet2)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.ConnectedFrom) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (host:Node {name:csvline.ConnectedFrom}) " \
               "MERGE (node:Node {name:csvline.ConnectedTo}) " \
               "CREATE (host)-[:connected]->(node)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.ResolvedIP) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (domain:DomainName {name:csvline.ResolvedDomain}) " \
               "MERGE (ip:IP {ipAddress:csvline.ResolvedIP}) " \
               "CREATE (ip)-[:resolvesTo {start:csvline.ResolvedStart, end:csvline.ResolvedEnd}]->(domain))"

    @staticmethod
    def add_detection_and_response_layer_nodes():
        return "LOAD CSV WITH HEADERS FROM \"file:///DetectionAndResponseLayerNodes.csv\" AS csvline " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.SecurityEventType) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:SecurityEvent {type:csvline.SecurityEvent, detectionTime:csvline.DetectionTime, " \
               "ceaseTime:csvline.CeaseTime, detectedTimes:csvline.DetectedTimes, " \
               "confirmed:csvline.Confirmed, description:csvline.Description})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.DetectionSystem) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:DetectionSystem {name:csvline.DetectionSystem})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.ObservationPoint) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:ObservationPoint {name:csvline.ObservationPoint})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.IncidentStart) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Incident {startTime:csvline.IncidentStart, " \
               "incidentEnd:csvline.IncidentEnd, severity:csvline.IncidentSeverity})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.ResponseType) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Response {responseType:csvline.ResponseType, start:csvline.ResponseStart, " \
               "end:csvline.ResponseEnd, parameters:csvline.ResponseParameters}))"

    @staticmethod
    def add_detection_and_response_layer_relationships():
        return "LOAD CSV WITH HEADERS FROM \"file:///DetectionAndResponseLayerRelationships.csv\" AS csvline " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.DataInputFrom) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (obpoint:ObservationPoint {name:csvline.DataInputFrom}) " \
               "MERGE (detsystem:DetectionSystem {name:csvline.DataInputTo}) " \
               "CREATE (obpoint)-[:dataInput]->(detsystem)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.RaisesFrom) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (det:DetectionSystem {name:csvline.RaisesFrom}) " \
               "MERGE (sec:SecurityEvent {detectionTime:csvline.RaisesTo}) " \
               "CREATE (det)-[:raises]->(sec)) F" \
               "OREACH(ignoreMe IN CASE WHEN trim(csvline.Relatesfrom) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (sec:SecurityEvent {detectionTime:csvline.Relatesfrom}) " \
               "MERGE (inc:Incident {startTime:csvline.Relatesto}) " \
               "CREATE (sec)-[:relatesTo]->(inc)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Relatesto) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (res:Response {start:csvline.ResponseFrom}) " \
               "MERGE (inc:Incident {startTime:csvline.Relatesto}) " \
               "CREATE (res)-[:responseTo]->(inc)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Observation) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (obs:ObservationPoint {name:csvline.Observation}) " \
               "MERGE (nod:Node {name:csvline.Node}) " \
               "CREATE (obs)-[:isA]->(nod)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Event) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (sec:SecurityEvent {detectionTime:csvline.Event}) " \
               "MERGE (ip:IP {ipAddress:csvline.Target}) " \
               "CREATE (sec)-[:target]->(ip))"

    @staticmethod
    def add_access_control_layer_nodes():
        return "LOAD CSV WITH HEADERS FROM \"file:///AccessLayerNodes.csv\" AS csvline " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Application) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Application {name:csvline.Application})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Device) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Device {name:csvline.Device})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Permission) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Permission {name:csvline.Permission})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Role) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Role {name:csvline.Role})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.User) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:User {name:csvline.User})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Group) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Group {name:csvline.Group})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.OrganizationUnit) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:OrganizationUnit {name:csvline.OrganizationUnit}))"

    @staticmethod
    def add_access_control_layer_relationships():
        return "LOAD CSV WITH HEADERS FROM \"file:///AccessLayerRelationships.csv\" AS csvline " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.ComponentHasIdentity) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (comp:Component {name:csvline.ComponentHasIdentity}) " \
               "MERGE (app:Application {name:csvline.OfApplicationName}) " \
               "CREATE (comp)-[:hasIdentity]->(app)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.HostHasIdentity) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (host:Host {name:csvline.HostHasIdentity}) " \
               "MERGE (dev:Device {name:csvline.OfDevice}) " \
               "CREATE (host)-[:hasIdentity]->(dev)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.PermissionTo) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (perm:Permission {name:csvline.PermissionTo}) " \
               "MERGE (app:Application {name:csvline.Application}) " \
               "CREATE (perm)-[:to]->(app)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.PermissionTo2) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (perm:Permission {name:csvline.PermissionTo2}) " \
               "MERGE (dev:Device {name:csvline.Device}) " \
               "CREATE (perm)-[:to]->(dev)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.RoleHas) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (rol:Role {name:csvline.RoleHas}) " \
               "MERGE (perm:Permission {name:csvline.Permission}) " \
               "CREATE (rol)-[:has]->(perm)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.UserAssigned) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (use:User {name:csvline.UserAssigned}) " \
               "MERGE (rol:Role {name:csvline.Role}) " \
               "CREATE (use)-[:assignedTo]->(rol)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.GroupAssignedTo) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (gro:Group {name:csvline.GroupAssignedTo}) " \
               "MERGE (rol:Role {name:csvline.Role2}) " \
               "CREATE (gro)-[:assignedTo]->(rol)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.UserToGroup) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (use:User {name:csvline.UserToGroup}) " \
               "MERGE (gro:Group {name:csvline.Group}) " \
               "CREATE (use)-[:memberOf]->(gro)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.DevicetoOrganizationUnit) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (dev:Device {name:csvline.DevicetoOrganizationUnit}) " \
               "MERGE (org:OrganizationUnit {name:csvline.OrganizationUnit}) " \
               "CREATE (dev)-[:partOf]->(org)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.UserToOrganizationalUnit) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (use:User {name:csvline.UserToOrganizationalUnit}) " \
               "MERGE (org:OrganizationUnit {name:csvline.OrgationalUnit2}) " \
               "CREATE (use)-[:partOf]->(org)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.GroupToOrganization) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (gro:Group {name:csvline.GroupToOrganization}) " \
               "MERGE (org:OrganizationUnit {name:csvline.OrganizationUnit3}) " \
               "CREATE (gro)-[:partOf]->(org)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.SubnetToOrganizationalUnit) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (sub:Subnet {subnet:csvline.SubnetToOrganizationalUnit}) " \
               "MERGE (org:OrganizationUnit {name:csvline.OrganizationUnit4}) " \
               "CREATE (sub)-[:partOf]->(org))"

    @staticmethod
    def add_mission_layer_nodes():
        return "LOAD CSV WITH HEADERS FROM \"file:///MissionLayerNodes.csv\" AS csvline " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Mission) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Mission {mission:csvline.Mission, criticality:csvline.Criticality})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.AvailabilityRequirement) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:AvailabilityRequirement {description:csvline.AvailabilityRequirement, " \
               "importanceLevel:csvline.AvailabilityImportanceLevel})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.ConfidentialityRequirement) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:ConfidentialityRequirement {description:csvline.ConfidentialityRequirement, " \
               "importanceLevel:csvline.ConfidentialityImportanceLevel})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.IntegrityRequirement) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:IntegrityRequirement {description:csvline.IntegrityRequirement, " \
               "importanceLevel:csvline.IntegrityImportanceLevel}))"

    @staticmethod
    def add_mission_layer_relationships():
        return "LOAD CSV WITH HEADERS FROM \"file:///MissionLayerRelationships.csv\" AS csvline " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.MissionImposes) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (miss:Mission {mission:csvline.MissionImposes}) " \
               "MERGE (ava:AvailabilityRequirement {description:csvline.Availability}) " \
               "CREATE (miss)-[:imposes]->(ava)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.MissionImposes) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (miss:Mission {mission:csvline.MissionImposes}) " \
               "MERGE (confi:ConfidentialityRequirement {description:csvline.Confidentiality}) " \
               "CREATE (miss)-[:imposes]->(confi)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.MissionImposes) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (miss:Mission {mission:csvline.MissionImposes}) " \
               "MERGE (inte:IntegrityRequirement {description:csvline.Integrity}) " \
               "CREATE (miss)-[:imposes]->(inte)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.MissionSupports) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (miss1:Mission {mission:csvline.MissionSupports}) " \
               "MERGE (miss2:Mission {mission:csvline.MissionReceivedSupport}) " \
               "CREATE (miss1)-[:supports]->(miss2)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.MissionSupportComponent) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (miss:Mission {mission:csvline.MissionSupportComponent}) " \
               "MERGE (comp:Component {name:csvline.ComponentReceivedSupport}) " \
               "CREATE (miss)-[:supports]->(comp)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.AvailabilityRequirementFor) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (ava:AvailabilityRequirement {description:csvline.AvailabilityRequirementFor}) " \
               "MERGE (org:OrganizationUnit {name:csvline.OrganizationUnit}) " \
               "CREATE (ava)-[:for]->(org)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.ConfidentialRequirementFor) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (confi:ConfidentialityRequirement {description:csvline.ConfidentialRequirementFor}) " \
               "MERGE (dat:Data {data:csvline.Data}) " \
               "CREATE (confi)-[:on]->(dat)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.ConfiRequirementOn) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (confi:ConfidentialityRequirement {description:csvline.ConfiRequirementOn}) " \
               "MERGE (comp:Component {name:csvline.Componento}) " \
               "CREATE (confi)-[:on]->(comp)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.IntegrityRequirmentOn) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (integ:IntegrityRequirement {description:csvline.IntegrityRequirmentOn}) " \
               "MERGE (dat:Data {data:csvline.Datas}) " \
               "CREATE (integ)-[:on]->(dat)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.IntegrityOns) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (inte:IntegrityRequirement {description:csvline.IntegrityOns}) " \
               "MERGE (comp:Component {name:csvline.ComponentIntegri}) " \
               "CREATE (inte)-[:on]->(comp)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.AvailaRequirementFor) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (ava:AvailabilityRequirement {description:csvline.AvailaRequirementFor}) " \
               "MERGE (dat:Data {data:csvline.Data3}) " \
               "CREATE (ava)-[:on]->(dat)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.AvaReqComponent) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (ava:AvailabilityRequirement {description:csvline.AvaReqComponent}) " \
               "MERGE (comp:Component {name:csvline.Component3}) " \
               "CREATE (ava)-[:on]->(comp))"

    @staticmethod
    def add_threat_layer_nodes():
        return "LOAD CSV WITH HEADERS FROM \"file:///ThreatLayerNodes.csv\" AS csvline " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.Vulnerability) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:Vulnerability {name:csvline.Vulnerability})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.SoftwareVersion) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:SoftwareVersion {version:csvline.SoftwareVersion})) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.CVE) <> \"\" THEN [1] ELSE [] END | " \
               "CREATE (:CVE {cve:csvline.CVE, cwe:csvline.CWE, cvss:csvline.CVSS, description:csvline.description}))"

    @staticmethod
    def add_threat_layer_relationships():
        return "LOAD CSV WITH HEADERS FROM \"file:///ThreatLayerRelationships.csv\" AS csvline " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.VulnerabilityIn) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (vuln:Vulnerability {name:csvline.VulnerabilityIn}) " \
               "MERGE (soft:SoftwareVersion {version:csvline.SoftwareV}) " \
               "CREATE (vuln)-[:in]->(soft)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.VulnerabilityIn) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (vuln:Vulnerability {name:csvline.VulnerabilityIn}) " \
               "MERGE (cve:CVE {cve:csvline.CVE}) " \
               "CREATE (vuln)-[:refersTo]->(cve)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.SoftwareResource) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (soft:SoftwareResource {name:csvline.SoftwareResource}) " \
               "MERGE (versi:SoftwareVersion {version:csvline.SoftVersion}) " \
               "CREATE (soft)-[:has]->(versi)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.VulnIn) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (vuln:Vulnerability {name:csvline.VulnIn}) " \
               "MERGE (soft:SoftwareResource {name:csvline.Software}) " \
               "CREATE (vuln)-[:in]->(soft)) " \
               "FOREACH(ignoreMe IN CASE WHEN trim(csvline.SecEvent) <> \"\" THEN [1] ELSE [] END | " \
               "MERGE (sec:SecurityEvent {detectionTime:csvline.SecEvent}) " \
               "MERGE (vuln:Vulnerability {name:csvline.Vuln}) " \
               "CREATE (sec)-[:refersTo]->(vuln))"
