create database ticket_system;
use ticket_system;


INSERT INTO trains VALUES (12760,'CHARMINAR EXPRESS', 'Hyderabad', 'Chennai', 792, 455, '18:00', '08:00');
INSERT INTO trains VALUES (12759,'CHARMINAR EXPRESS', 'Chennai', 'Hyderabad', 792, 455, '17:30', '08:10');

INSERT INTO trains VALUES (22159,'CHENNAI EXPRESS', 'Mumbai', 'Chennai', 936, 595, '12:45', '10:45');
INSERT INTO trains VALUES (22160,'CHENNAI EXPRESS', 'Chennai', 'Mumbai', 936, 595, '13:15', '12:30');

INSERT INTO trains VALUES (12622,'TAMILNADU EXPRESS', 'Delhi', 'Chennai', 864, 820, '21:05', '06:35');
INSERT INTO trains VALUES (12621,'TAMILNADU EXPRESS', 'Chennai', 'Delhi', 864, 820, '22:00', '06:30');

INSERT INTO trains VALUES (12615,'GRAND TRUNK EXPRESS', 'Chennai', 'Delhi', 425, 820, '17:40', '05:05');
INSERT INTO trains VALUES (12616,'GRAND TRUNK EXPRESS', 'Delhi', 'Chennai', 425, 820, '16:10', '05:00');


select * from trains;