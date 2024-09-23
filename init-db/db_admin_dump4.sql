--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: AnonymousUser; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."AnonymousUser" (
    username character varying NOT NULL,
    id integer NOT NULL,
    created_at character varying NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public."AnonymousUser" OWNER TO admin;

--
-- Name: AnonymousUser_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."AnonymousUser_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."AnonymousUser_id_seq" OWNER TO admin;

--
-- Name: AnonymousUser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."AnonymousUser_id_seq" OWNED BY public."AnonymousUser".id;


--
-- Name: Token; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Token" (
    hash character varying NOT NULL,
    expiration timestamp without time zone NOT NULL,
    id integer NOT NULL,
    created_at character varying NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public."Token" OWNER TO admin;

--
-- Name: Token_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Token_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Token_id_seq" OWNER TO admin;

--
-- Name: Token_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Token_id_seq" OWNED BY public."Token".id;


--
-- Name: article; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.article (
    name character varying NOT NULL,
    slug character varying NOT NULL,
    intro_text character varying NOT NULL,
    bid_approved boolean NOT NULL,
    count_views integer NOT NULL,
    title character varying NOT NULL,
    user_id integer NOT NULL,
    disable boolean NOT NULL,
    id integer NOT NULL,
    created_at character varying NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.article OWNER TO admin;

--
-- Name: article_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.article_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.article_id_seq OWNER TO admin;

--
-- Name: article_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.article_id_seq OWNED BY public.article.id;


--
-- Name: code; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.code (
    code integer NOT NULL,
    email character varying NOT NULL,
    id integer NOT NULL,
    created_at character varying NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.code OWNER TO admin;

--
-- Name: code_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.code_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.code_id_seq OWNER TO admin;

--
-- Name: code_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.code_id_seq OWNED BY public.code.id;


--
-- Name: comment; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.comment (
    content character varying NOT NULL,
    user_id integer NOT NULL,
    article_id integer NOT NULL,
    id integer NOT NULL,
    created_at character varying NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.comment OWNER TO admin;

--
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comment_id_seq OWNER TO admin;

--
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."user" (
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    email character varying,
    password character varying NOT NULL,
    username character varying NOT NULL,
    is_admin_user boolean NOT NULL,
    id integer NOT NULL,
    created_at character varying NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public."user" OWNER TO admin;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO admin;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: AnonymousUser id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."AnonymousUser" ALTER COLUMN id SET DEFAULT nextval('public."AnonymousUser_id_seq"'::regclass);


--
-- Name: Token id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Token" ALTER COLUMN id SET DEFAULT nextval('public."Token_id_seq"'::regclass);


--
-- Name: article id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.article ALTER COLUMN id SET DEFAULT nextval('public.article_id_seq'::regclass);


--
-- Name: code id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.code ALTER COLUMN id SET DEFAULT nextval('public.code_id_seq'::regclass);


--
-- Name: comment id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: AnonymousUser; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public."AnonymousUser" (username, id, created_at, updated_at) FROM stdin;
AnonymousUser	1	2023-09-02T17:31:25.857666	2023-09-02 17:31:25.857666+00
\.


--
-- Data for Name: Token; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public."Token" (hash, expiration, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: article; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.article (name, slug, intro_text, bid_approved, count_views, title, user_id, disable, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: code; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.code (code, email, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.comment (content, user_id, article_id, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public."user" (first_name, last_name, email, password, username, is_admin_user, id, created_at, updated_at) FROM stdin;
Админ	Админович	naaro2930@gmail.com	$2b$12$3XdXSNyLFlRryEP0d7my5uztS0ZKiH0S9O.6ym8OmS6DlP56wXtWm	admin	t	1	2024-09-23 13:25:05.617797+00	2024-09-23 13:25:05.617797+00
\.


--
-- Name: AnonymousUser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public."AnonymousUser_id_seq"', 1, false);


--
-- Name: Token_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public."Token_id_seq"', 1, false);


--
-- Name: article_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.article_id_seq', 1, false);


--
-- Name: code_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.code_id_seq', 1, false);


--
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.comment_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.user_id_seq', 1, true);


--
-- Name: AnonymousUser AnonymousUser_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."AnonymousUser"
    ADD CONSTRAINT "AnonymousUser_pkey" PRIMARY KEY (id);


--
-- Name: AnonymousUser AnonymousUser_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."AnonymousUser"
    ADD CONSTRAINT "AnonymousUser_username_key" UNIQUE (username);


--
-- Name: Token Token_hash_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Token"
    ADD CONSTRAINT "Token_hash_key" UNIQUE (hash);


--
-- Name: Token Token_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Token"
    ADD CONSTRAINT "Token_pkey" PRIMARY KEY (id);


--
-- Name: article article_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.article
    ADD CONSTRAINT article_pkey PRIMARY KEY (id);


--
-- Name: article article_slug_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.article
    ADD CONSTRAINT article_slug_key UNIQUE (slug);


--
-- Name: code code_code_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.code
    ADD CONSTRAINT code_code_key UNIQUE (code);


--
-- Name: code code_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.code
    ADD CONSTRAINT code_pkey PRIMARY KEY (id);


--
-- Name: comment comment_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_pkey PRIMARY KEY (id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: ix_AnonymousUser_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX "ix_AnonymousUser_id" ON public."AnonymousUser" USING btree (id);


--
-- Name: ix_Token_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX "ix_Token_id" ON public."Token" USING btree (id);


--
-- Name: ix_article_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_article_id ON public.article USING btree (id);


--
-- Name: ix_article_name; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_article_name ON public.article USING btree (name);


--
-- Name: ix_article_title; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_article_title ON public.article USING btree (title);


--
-- Name: ix_code_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_code_id ON public.code USING btree (id);


--
-- Name: ix_comment_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_comment_id ON public.comment USING btree (id);


--
-- Name: ix_user_first_name; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_user_first_name ON public."user" USING btree (first_name);


--
-- Name: ix_user_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_user_id ON public."user" USING btree (id);


--
-- Name: ix_user_last_name; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_user_last_name ON public."user" USING btree (last_name);


--
-- Name: article article_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.article
    ADD CONSTRAINT article_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: comment comment_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_article_id_fkey FOREIGN KEY (article_id) REFERENCES public.article(id);


--
-- Name: comment comment_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

