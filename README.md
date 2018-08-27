# CRUSOE Data Model Example Database

This repo contains an example of CRUSOE data model filled with mock data. This data model was presented in the paper "CRUSOE: Data Model for Cyber Situational Awareness" on International Workshop on Cyber Threat Intelligence (WCTI 2018) held in conjunction with the 13th International Conference on Availability, Reliability and Security (ARES 2018).

To install the database with data model, just download/clone this repo a write command 

```
vagrant up
```

Everything will setup automatically and the database will start on Neo4j default port - http://localhost:7474/ - with the following credentials:

```
username: neo4j
password: neo4jAres
```

This repo also contains a beautifier *style.grass* which provides Neo4j frontend a style with nice colors to browse the data. To use it, just drag-and-drop this file into import section of Neo4j frontend.

To quickly scan through the database and see the data model example, you can see the screenshots in Pictures folder.

## Reference

KOMÁRKOVÁ, Jana, Martin HUSÁK, Martin LAŠTOVIČKA a Daniel TOVARŇÁK. CRUSOE: Data Model for Cyber Situation Awareness. In Proceedings of the 13th International Conference on Availability, Reliability and Security. Hamburg: ACM, 2018. s. "36:1--36:10", 10 s. ISBN 978-1-4503-6448-5. doi:10.1145/3230833.3232798.
