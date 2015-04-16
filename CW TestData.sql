insert into Staff
Values
(1, 'staffname1'),
(2, 'staffname2'),
(3, 'staffname3'),
(4, 'staffname4'),
(5, 'staffname5');

insert into Product
Values
(10, 'Product10'),
(11, 'Product11'),
(12, 'Product12'),
(13, 'Product13'),
(14, 'Product14'),
(15, 'Product15');

insert into Customer
Values
(100, 'Customer100', 'Customeremail100'),
(101, 'Customer101', 'Customeremail101'),
(102, 'Customer102', 'Customeremail102'),
(103, 'Customer103', 'Customeremail103'),
(104, 'Customer104', 'Customeremail104'),
(105, 'Customer105', 'Customeremail105');

insert into Ticket(TicketID, Problem, Priority, LoggedTime, CustomerID, ProductID)
Values
(50, 'broke50', 2, NOW(), 104, 14),
(51, 'broke51', 1, NOW(), 102, 10),
(52, 'broke52', 3, NOW(), 103, 11),
(53, 'broke53', 1, NOW(), 102, 12),
(54, 'broke54', 2, NOW(), 102, 12),
(55, 'broke55', 2, NOW(), 101, 15);


insert into TicketUpdate
Values
(71, 'fixed71', NOW(), 52, 3),
(72, 'fixed72', NOW(), 51, 1),
(73, 'fixed73', NOW(), 53, 2),
(74, 'fixed74', NOW(), 52, 5),
(75, 'fixed75', NOW(), 54, 1);