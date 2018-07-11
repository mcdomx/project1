-- Adminer 4.6.3-dev PostgreSQL dump

\connect "d6avrg1hsn8aje";

DROP TABLE IF EXISTS "tbl_comments";
DROP SEQUENCE IF EXISTS tbl_comments_comment_id_seq;
CREATE SEQUENCE tbl_comments_comment_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."tbl_comments" (
    "comment_id" integer DEFAULT nextval('tbl_comments_comment_id_seq') NOT NULL,
    "cmt_date" date,
    "user_id" character varying,
    "zipcode" character varying,
    "comment" character varying,
    CONSTRAINT "tbl_comments_pkey" PRIMARY KEY ("comment_id"),
    CONSTRAINT "tbl_comments_user_id_fkey" FOREIGN KEY (user_id) REFERENCES tbl_users(user_id) NOT DEFERRABLE,
    CONSTRAINT "tbl_comments_zipcode_fkey" FOREIGN KEY (zipcode) REFERENCES tbl_locations(zipcode) NOT DEFERRABLE
) WITH (oids = false);


DROP TABLE IF EXISTS "tbl_locations";
CREATE TABLE "public"."tbl_locations" (
    "zipcode" character varying NOT NULL,
    "city" character varying NOT NULL,
    "state" character varying NOT NULL,
    "lat" double precision NOT NULL,
    "lon" double precision NOT NULL,
    "population" integer NOT NULL,
    CONSTRAINT "tbl_locations_pkey" PRIMARY KEY ("zipcode")
) WITH (oids = false);


DROP TABLE IF EXISTS "tbl_users";
CREATE TABLE "public"."tbl_users" (
    "user_id" character varying NOT NULL,
    "name" character varying NOT NULL,
    "password" character varying NOT NULL,
    CONSTRAINT "tbl_users_pkey" PRIMARY KEY ("user_id")
) WITH (oids = false);


-- 2018-07-11 20:14:21.037226+00
