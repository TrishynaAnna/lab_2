/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/* Created on:     25.10.2019 18:01:24                          */
/*==============================================================*/


drop index Groups_PK;

drop table Groups;

drop index Groups_Posts2_FK;

drop index Groups_Posts_FK;

drop index Groups_Posts_PK;

drop table Groups_Posts;

drop index Posts_Notification_FK;

drop index Notificstion_PK;

drop table Notificstion;

drop index Posts_PK;

drop table Posts;

drop index User_PK;

drop table "User";

drop index User_Groups2_FK;

drop index User_Groups_FK;

drop index User_Groups_PK;

drop table User_Groups;

/*==============================================================*/
/* Table: Groups                                                */
/*==============================================================*/
create table Groups (
   group_id             NUMERIC(10)          not null,
   group_name           VARCHAR(20)          null,
   group_topic          VARCHAR(20)          null,
   constraint PK_GROUPS primary key (group_id)
);

/*==============================================================*/
/* Index: Groups_PK                                             */
/*==============================================================*/
create unique index Groups_PK on Groups (
group_id
);

/*==============================================================*/
/* Table: Groups_Posts                                          */
/*==============================================================*/
create table Groups_Posts (
   group_id             NUMERIC(10)          not null,
   post_id              NUMERIC(10)          not null,
   constraint PK_GROUPS_POSTS primary key (group_id, post_id)
);

/*==============================================================*/
/* Index: Groups_Posts_PK                                       */
/*==============================================================*/
create unique index Groups_Posts_PK on Groups_Posts (
group_id,
post_id
);

/*==============================================================*/
/* Index: Groups_Posts_FK                                       */
/*==============================================================*/
create  index Groups_Posts_FK on Groups_Posts (
group_id
);

/*==============================================================*/
/* Index: Groups_Posts2_FK                                      */
/*==============================================================*/
create  index Groups_Posts2_FK on Groups_Posts (
post_id
);

/*==============================================================*/
/* Table: Notificstion                                          */
/*==============================================================*/
create table Notificstion (
   notification_id      NUMERIC(10)          not null,
   post_id              NUMERIC(10)          null,
   notification_time    VARCHAR(5)           null,
   notification_text    VARCHAR(100)         null,
   constraint PK_NOTIFICSTION primary key (notification_id)
);

/*==============================================================*/
/* Index: Notificstion_PK                                       */
/*==============================================================*/
create unique index Notificstion_PK on Notificstion (
notification_id
);

/*==============================================================*/
/* Index: Posts_Notification_FK                                 */
/*==============================================================*/
create  index Posts_Notification_FK on Notificstion (
post_id
);

/*==============================================================*/
/* Table: Posts                                                 */
/*==============================================================*/
create table Posts (
   post_id              NUMERIC(10)          not null,
   post_content         VARCHAR(10000)       null,
   post_hashtag         VARCHAR(20)          null,
   constraint PK_POSTS primary key (post_id)
);

/*==============================================================*/
/* Index: Posts_PK                                              */
/*==============================================================*/
create unique index Posts_PK on Posts (
post_id
);

/*==============================================================*/
/* Table: "User"                                                */
/*==============================================================*/
create table "User" (
   id_user              NUMERIC(10)          not null,
   name_user            VARCHAR(20)          null,
   constraint PK_USER primary key (id_user)
);

/*==============================================================*/
/* Index: User_PK                                               */
/*==============================================================*/
create unique index User_PK on "User" (
id_user
);

/*==============================================================*/
/* Table: User_Groups                                           */
/*==============================================================*/
create table User_Groups (
   id_user              NUMERIC(10)          not null,
   group_id             NUMERIC(10)          not null,
   constraint PK_USER_GROUPS primary key (id_user, group_id)
);

/*==============================================================*/
/* Index: User_Groups_PK                                        */
/*==============================================================*/
create unique index User_Groups_PK on User_Groups (
id_user,
group_id
);

/*==============================================================*/
/* Index: User_Groups_FK                                        */
/*==============================================================*/
create  index User_Groups_FK on User_Groups (
id_user
);

/*==============================================================*/
/* Index: User_Groups2_FK                                       */
/*==============================================================*/
create  index User_Groups2_FK on User_Groups (
group_id
);

alter table Groups_Posts
   add constraint FK_GROUPS_P_GROUPS_PO_GROUPS foreign key (group_id)
      references Groups (group_id)
      on delete restrict on update restrict;

alter table Groups_Posts
   add constraint FK_GROUPS_P_GROUPS_PO_POSTS foreign key (post_id)
      references Posts (post_id)
      on delete restrict on update restrict;

alter table Notificstion
   add constraint FK_NOTIFICS_POSTS_NOT_POSTS foreign key (post_id)
      references Posts (post_id)
      on delete restrict on update restrict;

alter table User_Groups
   add constraint FK_USER_GRO_USER_GROU_USER foreign key (id_user)
      references "User" (id_user)
      on delete restrict on update restrict;

alter table User_Groups
   add constraint FK_USER_GRO_USER_GROU_GROUPS foreign key (group_id)
      references Groups (group_id)
      on delete restrict on update restrict;

