create table Board
(
	board_id int unsigned auto_increment,
	full_sn varchar(15) not null,
	type_sn int(6) not null,
	type_code varchar(6) not null,
	sn int(6) not null,
	major_type_id int unsigned,
	sub_type_id int unsigned, 
	primary key (board_id),
	unique(full_sn)
);

create table Major_Type
(
	major_type_id int unsigned auto_increment,
	primary key (major_type_id),
	name varchar(50) not null,
	major_sn int(2) unsigned not null,
	major_code varchar(2) not null
);

create table Sub_Type
(
	sub_type_id int unsigned auto_increment,
	primary key (sub_type_id),
	sub_sn int(4) unsigned not null,
	sub_code varchar(4) not null,
	name varchar(50) not null,
	identifyer_name varchar(10) not null

);

create table Major_Sub_Stitch
(
	major_type_id int unsigned,
	sub_type_id int unsigned
);
