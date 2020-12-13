--
-- petr_kurilQL database dump
--

-- Dumped from database version 12.4
-- Dumped by pg_dump version 12.4

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

--
-- Name: logistics; Type: DATABASE; Schema: -; Owner: petr_kuril
--

CREATE DATABASE logistics WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Russian_Russia.1251' LC_CTYPE = 'Russian_Russia.1251';


ALTER DATABASE logistics OWNER TO petr_kuril;

\connect logistics

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: petr_kuril
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO petr_kuril;

--
-- Name: applications; Type: TABLE; Schema: public; Owner: petr_kuril
--

CREATE TABLE public.applications (
    application_id integer NOT NULL,
    name character varying(128) NOT NULL,
    conclusion_date date NOT NULL,
    delivery_route integer,
    shipper_id integer,
    receiver_id integer,
    status character varying(9) NOT NULL
);


ALTER TABLE public.applications OWNER TO petr_kuril;

--
-- Name: applications_application_id_seq; Type: SEQUENCE; Schema: public; Owner: petr_kuril
--

CREATE SEQUENCE public.applications_application_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.applications_application_id_seq OWNER TO petr_kuril;

--
-- Name: applications_application_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: petr_kuril
--

ALTER SEQUENCE public.applications_application_id_seq OWNED BY public.applications.application_id;


--
-- Name: blacklist_tokens; Type: TABLE; Schema: public; Owner: petr_kuril
--

CREATE TABLE public.blacklist_tokens (
    id integer NOT NULL,
    token character varying(500) NOT NULL,
    blacklisted_on timestamp without time zone
);


ALTER TABLE public.blacklist_tokens OWNER TO petr_kuril;

--
-- Name: blacklist_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: petr_kuril
--

CREATE SEQUENCE public.blacklist_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blacklist_tokens_id_seq OWNER TO petr_kuril;

--
-- Name: blacklist_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: petr_kuril
--

ALTER SEQUENCE public.blacklist_tokens_id_seq OWNED BY public.blacklist_tokens.id;


--
-- Name: cargos; Type: TABLE; Schema: public; Owner: petr_kuril
--

CREATE TABLE public.cargos (
    cargo_id integer NOT NULL,
    nomenclature character varying(64) NOT NULL,
    weight double precision NOT NULL,
    application_id integer
);


ALTER TABLE public.cargos OWNER TO petr_kuril;

--
-- Name: cargos_cargo_id_seq; Type: SEQUENCE; Schema: public; Owner: petr_kuril
--

CREATE SEQUENCE public.cargos_cargo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cargos_cargo_id_seq OWNER TO petr_kuril;

--
-- Name: cargos_cargo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: petr_kuril
--

ALTER SEQUENCE public.cargos_cargo_id_seq OWNED BY public.cargos.cargo_id;


--
-- Name: cars; Type: TABLE; Schema: public; Owner: petr_kuril
--

CREATE TABLE public.cars (
    car_id integer NOT NULL,
    weight double precision NOT NULL,
    volume double precision NOT NULL,
    model character varying(64) NOT NULL,
    category character varying(1) NOT NULL
);


ALTER TABLE public.cars OWNER TO petr_kuril;

--
-- Name: cars_applications; Type: TABLE; Schema: public; Owner: petr_kuril
--

CREATE TABLE public.cars_applications (
    car_id integer,
    application_id integer,
    cars_applications_id integer NOT NULL
);


ALTER TABLE public.cars_applications OWNER TO petr_kuril;

--
-- Name: cars_applications_cars_applications_id_seq; Type: SEQUENCE; Schema: public; Owner: petr_kuril
--

ALTER TABLE public.cars_applications ALTER COLUMN cars_applications_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.cars_applications_cars_applications_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cars_car_id_seq; Type: SEQUENCE; Schema: public; Owner: petr_kuril
--

CREATE SEQUENCE public.cars_car_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cars_car_id_seq OWNER TO petr_kuril;

--
-- Name: cars_car_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: petr_kuril
--

ALTER SEQUENCE public.cars_car_id_seq OWNED BY public.cars.car_id;


--
-- Name: clients; Type: TABLE; Schema: public; Owner: petr_kuril
--

CREATE TABLE public.clients (
    client_id integer NOT NULL,
    passport_number integer NOT NULL,
    passport_series integer NOT NULL,
    first_name character varying(32) NOT NULL,
    last_name character varying(32) NOT NULL,
    middle_name character varying(32),
    email character varying(32),
    phone character varying(11) NOT NULL
);


ALTER TABLE public.clients OWNER TO petr_kuril;

--
-- Name: clients_client_id_seq; Type: SEQUENCE; Schema: public; Owner: petr_kuril
--

CREATE SEQUENCE public.clients_client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.clients_client_id_seq OWNER TO petr_kuril;

--
-- Name: clients_client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: petr_kuril
--

ALTER SEQUENCE public.clients_client_id_seq OWNED BY public.clients.client_id;


--
-- Name: contacts; Type: TABLE; Schema: public; Owner: petr_kuril
--

CREATE TABLE public.contacts (
    contact_id integer NOT NULL,
    first_name character varying(32) NOT NULL,
    last_name character varying(32) NOT NULL,
    middle_name character varying(32),
    "position" character varying(32),
    organization character varying(64),
    phone character varying(11) NOT NULL
);


ALTER TABLE public.contacts OWNER TO petr_kuril;

--
-- Name: contacts_contact_id_seq; Type: SEQUENCE; Schema: public; Owner: petr_kuril
--

CREATE SEQUENCE public.contacts_contact_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contacts_contact_id_seq OWNER TO petr_kuril;

--
-- Name: contacts_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: petr_kuril
--

ALTER SEQUENCE public.contacts_contact_id_seq OWNED BY public.contacts.contact_id;


--
-- Name: contracts; Type: TABLE; Schema: public; Owner: petr_kuril
--

CREATE TABLE public.contracts (
    contract_id integer NOT NULL,
    conclusion_date date NOT NULL,
    cost numeric(10,2) NOT NULL,
    payment_type character varying(32),
    client_id integer,
    application_id integer,
    requisite_id integer
);


ALTER TABLE public.contracts OWNER TO petr_kuril;

--
-- Name: contracts_contract_id_seq; Type: SEQUENCE; Schema: public; Owner: petr_kuril
--

CREATE SEQUENCE public.contracts_contract_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contracts_contract_id_seq OWNER TO petr_kuril;

--
-- Name: contracts_contract_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: petr_kuril
--

ALTER SEQUENCE public.contracts_contract_id_seq OWNED BY public.contracts.contract_id;


--
-- Name: drivers; Type: TABLE; Schema: public; Owner: petr_kuril
--

CREATE TABLE public.drivers (
    driver_id integer NOT NULL,
    first_name character varying(32) NOT NULL,
    last_name character varying(32) NOT NULL,
    middle_name character varying(32),
    categories character varying[] NOT NULL,
    phone character varying(11) NOT NULL
);


ALTER TABLE public.drivers OWNER TO petr_kuril;

--
-- Name: drivers_applications; Type: TABLE; Schema: public; Owner: petr_kuril
--

CREATE TABLE public.drivers_applications (
    driver_id integer,
    application_id integer,
    drivers_applications_id integer NOT NULL
);


ALTER TABLE public.drivers_applications OWNER TO petr_kuril;

--
-- Name: drivers_applications_drivers_applications_id_seq; Type: SEQUENCE; Schema: public; Owner: petr_kuril
--

ALTER TABLE public.drivers_applications ALTER COLUMN drivers_applications_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.drivers_applications_drivers_applications_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: drivers_driver_id_seq; Type: SEQUENCE; Schema: public; Owner: petr_kuril
--

CREATE SEQUENCE public.drivers_driver_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.drivers_driver_id_seq OWNER TO petr_kuril;

--
-- Name: drivers_driver_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: petr_kuril
--

ALTER SEQUENCE public.drivers_driver_id_seq OWNED BY public.drivers.driver_id;


--
-- Name: requisites; Type: TABLE; Schema: public; Owner: petr_kuril
--

CREATE TABLE public.requisites (
    requisite_id integer NOT NULL,
    bank_name character varying(64) NOT NULL,
    "BIK" character varying(9) NOT NULL,
    "INN" character varying(10) NOT NULL,
    "KPP" character varying(9) NOT NULL,
    "KS" character varying(20) NOT NULL,
    "RS" character varying(20) NOT NULL,
    bank_account character varying(20) NOT NULL
);


ALTER TABLE public.requisites OWNER TO petr_kuril;

--
-- Name: requisites_requisite_id_seq; Type: SEQUENCE; Schema: public; Owner: petr_kuril
--

CREATE SEQUENCE public.requisites_requisite_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.requisites_requisite_id_seq OWNER TO petr_kuril;

--
-- Name: requisites_requisite_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: petr_kuril
--

ALTER SEQUENCE public.requisites_requisite_id_seq OWNED BY public.requisites.requisite_id;


--
-- Name: routes; Type: TABLE; Schema: public; Owner: petr_kuril
--

CREATE TABLE public.routes (
    route_id integer NOT NULL,
    delivery_address character varying(128),
    shipping_address character varying(128),
    distance double precision,
    estimated_time integer
);


ALTER TABLE public.routes OWNER TO petr_kuril;

--
-- Name: routes_route_id_seq; Type: SEQUENCE; Schema: public; Owner: petr_kuril
--

CREATE SEQUENCE public.routes_route_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.routes_route_id_seq OWNER TO petr_kuril;

--
-- Name: routes_route_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: petr_kuril
--

ALTER SEQUENCE public.routes_route_id_seq OWNED BY public.routes.route_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: petr_kuril
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    registered_on timestamp without time zone,
    admin boolean
);


ALTER TABLE public.users OWNER TO petr_kuril;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: petr_kuril
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO petr_kuril;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: petr_kuril
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: applications application_id; Type: DEFAULT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.applications ALTER COLUMN application_id SET DEFAULT nextval('public.applications_application_id_seq'::regclass);


--
-- Name: blacklist_tokens id; Type: DEFAULT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.blacklist_tokens ALTER COLUMN id SET DEFAULT nextval('public.blacklist_tokens_id_seq'::regclass);


--
-- Name: cargos cargo_id; Type: DEFAULT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.cargos ALTER COLUMN cargo_id SET DEFAULT nextval('public.cargos_cargo_id_seq'::regclass);


--
-- Name: cars car_id; Type: DEFAULT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.cars ALTER COLUMN car_id SET DEFAULT nextval('public.cars_car_id_seq'::regclass);


--
-- Name: clients client_id; Type: DEFAULT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.clients ALTER COLUMN client_id SET DEFAULT nextval('public.clients_client_id_seq'::regclass);


--
-- Name: contacts contact_id; Type: DEFAULT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.contacts ALTER COLUMN contact_id SET DEFAULT nextval('public.contacts_contact_id_seq'::regclass);


--
-- Name: contracts contract_id; Type: DEFAULT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.contracts ALTER COLUMN contract_id SET DEFAULT nextval('public.contracts_contract_id_seq'::regclass);


--
-- Name: drivers driver_id; Type: DEFAULT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.drivers ALTER COLUMN driver_id SET DEFAULT nextval('public.drivers_driver_id_seq'::regclass);


--
-- Name: requisites requisite_id; Type: DEFAULT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.requisites ALTER COLUMN requisite_id SET DEFAULT nextval('public.requisites_requisite_id_seq'::regclass);


--
-- Name: routes route_id; Type: DEFAULT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.routes ALTER COLUMN route_id SET DEFAULT nextval('public.routes_route_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: petr_kuril
--

COPY public.alembic_version (version_num) FROM stdin;
cf5f6f2aa36d
\.


--
-- Data for Name: applications; Type: TABLE DATA; Schema: public; Owner: petr_kuril
--

COPY public.applications (application_id, name, conclusion_date, delivery_route, shipper_id, receiver_id, status) FROM stdin;
5	Доставка огромной коллекции разноцветных членов на присосках со встроенным вибратором	2020-10-23	3	2	2	active
3	Дилдо (100 штук)	2020-11-30	2	4	4	active
4	Joint запрос	2020-11-25	1	3	3	active
1	Доставка чего-то	2020-11-20	6	1	1	active
2	Телевизор	2020-12-12	5	5	5	finished
7	wqeqasd	2020-11-25	3	2	2	active
8	asdasd	2020-12-03	3	2	2	active
\.


--
-- Data for Name: blacklist_tokens; Type: TABLE DATA; Schema: public; Owner: petr_kuril
--

COPY public.blacklist_tokens (id, token, blacklisted_on) FROM stdin;
\.


--
-- Data for Name: cargos; Type: TABLE DATA; Schema: public; Owner: petr_kuril
--

COPY public.cargos (cargo_id, nomenclature, weight, application_id) FROM stdin;
1	Дилдо	156.23	3
3	Телевизор	40	2
4	Холодильник ЗИЛ	60	1
2	Joint	0.17	4
\.


--
-- Data for Name: cars; Type: TABLE DATA; Schema: public; Owner: petr_kuril
--

COPY public.cars (car_id, weight, volume, model, category) FROM stdin;
1	3500	25	MAN	D
4	3500	21	MAN	D
3	2500	30	FOX	D
5	2000	15	Mercedes	E
6	1800	18	Mercedes	E
\.


--
-- Data for Name: cars_applications; Type: TABLE DATA; Schema: public; Owner: petr_kuril
--

COPY public.cars_applications (car_id, application_id, cars_applications_id) FROM stdin;
1	5	1
6	2	2
3	1	3
4	3	4
5	4	5
\.


--
-- Data for Name: clients; Type: TABLE DATA; Schema: public; Owner: petr_kuril
--

COPY public.clients (client_id, passport_number, passport_series, first_name, last_name, middle_name, email, phone) FROM stdin;
2	5819	499601	Евстрахий	Полено	Петрович	EfstrahTheLog@mail.ru	79162185692
1	4526	588761	Афонт	Семендяев	Константинович	afont@gmail.com	79854751892
3	4478	512485	Аббоссали	Мовсисян	Мунарбекович	abbossali1976@mail.ru	79856832385
4	7613	899417	Бибиб	Бердымухамедоф	Мяликгулыевич	dark_knight@vostok.com	79253859851
6	4478	499601	asdfasdf	asdf	wpoierhs	test@mail.ru	79856692385
\.


--
-- Data for Name: contacts; Type: TABLE DATA; Schema: public; Owner: petr_kuril
--

COPY public.contacts (contact_id, first_name, last_name, middle_name, "position", organization, phone) FROM stdin;
3	Гипопотам	Патопов	Потапович	Директор	ООО "Резервуар"	89851177813
4	Зевала	Отрыжкин	Алексеевич	Проходимец	ОПГ "Восточное"	89161762445
5	Владлен	Баррикадович	Ульянов	Революционер	\N	89855623891
2	Артём\n	Студнев	Викторович\n	Сторож	\N	89165069855
1	Максим	Бобров\n	Петрович	Лесоруб	\N	89160482409
7	Олег	Капустин	Семёнович	Разнорабочий	\N	89168088379
6	Джо-Биб	Маглиб	Младший	Налётчик	\N	89810978019
\.


--
-- Data for Name: contracts; Type: TABLE DATA; Schema: public; Owner: petr_kuril
--

COPY public.contracts (contract_id, conclusion_date, cost, payment_type, client_id, application_id, requisite_id) FROM stdin;
1	2020-11-04	48685.92	Card	1	5	2
3	2020-11-01	85650.00	Cash	3	3	4
7	2020-11-25	485.92	Card	1	7	2
4	2020-09-18	19999.99	Card	4	2	5
2	2020-11-28	19992.99	Cash	4	4	5
\.


--
-- Data for Name: drivers; Type: TABLE DATA; Schema: public; Owner: petr_kuril
--

COPY public.drivers (driver_id, first_name, last_name, middle_name, categories, phone) FROM stdin;
10	Абдумажит	Вахобович	Мухмагомедович	{'B','D','E'}	79168684849
11	Срапион	Мовсисян	Ваники	{'B','D'}	89858591451
12	awrq	qwrqw	qweqweq	{'B','E'}	74129581499
2	Атманда	Пивницкий	Мурзоевич	{'B','D','E','F'}	79997482464
8	Пётр	Водило	Азбекович	{'A','B','D'}	79164152616
9	Хайитбой	Зокиржон угли	Хамзанович	{'A','B','D','E','F'}	79259569153
\.


--
-- Data for Name: drivers_applications; Type: TABLE DATA; Schema: public; Owner: petr_kuril
--

COPY public.drivers_applications (driver_id, application_id, drivers_applications_id) FROM stdin;
8	2	3
9	3	4
10	4	5
11	1	6
12	2	9
2	5	10
\.


--
-- Data for Name: requisites; Type: TABLE DATA; Schema: public; Owner: petr_kuril
--

COPY public.requisites (requisite_id, bank_name, "BIK", "INN", "KPP", "KS", "RS", bank_account) FROM stdin;
2	ПАО СБЕРБАНК	044525225	7707083893	773601001	30101810400000000225	1485	76965594261126261716
3	ОАО ВТБ	740551822	7707015127	773850152	30108559100000000857	6558	75572169756+96436874
4	ООО ДжетМани	152850124	7707096124	773956124	30107592500000000982	6472	68418621653546874198
5	ООО АльфаБанк	850168842	7707085015	773755519	30107125400000000428	1537	35896843557869168685
\.


--
-- Data for Name: routes; Type: TABLE DATA; Schema: public; Owner: petr_kuril
--

COPY public.routes (route_id, delivery_address, shipping_address, distance, estimated_time) FROM stdin;
2	Шоссе Энтузиастов	Дом Семёна	245	60
3	Дом Семёна	Дом Руслана	8500	240
4	Дом Руслана	РТУ МИРЭА	4500	78
5	Дом Семёна	Подвал МГУПИ	6700	123
6	Откуда-то	Куда-то	440	45
1	asd	adas	951	147
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: petr_kuril
--

COPY public.users (id, email, password, registered_on, admin) FROM stdin;
1	johnn_d@mail.ru	$2b$04$Fxbt9/WEJsPXRxfNYjpxv.sBKFD1gPEE/ItTWsJkmecxl2VXGx66O	2020-11-24 23:20:25.187925	f
2	the_log@mail.ru	$2b$04$XjKDnJl1guEnw7bnVlpBc.UPqN6KmJ5f8vrM7gi08gDyJisClGAoK	2020-11-24 23:49:07.166632	f
\.


--
-- Name: applications_application_id_seq; Type: SEQUENCE SET; Schema: public; Owner: petr_kuril
--

SELECT pg_catalog.setval('public.applications_application_id_seq', 8, true);


--
-- Name: blacklist_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: petr_kuril
--

SELECT pg_catalog.setval('public.blacklist_tokens_id_seq', 1, false);


--
-- Name: cargos_cargo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: petr_kuril
--

SELECT pg_catalog.setval('public.cargos_cargo_id_seq', 6, true);


--
-- Name: cars_applications_cars_applications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: petr_kuril
--

SELECT pg_catalog.setval('public.cars_applications_cars_applications_id_seq', 7, true);


--
-- Name: cars_car_id_seq; Type: SEQUENCE SET; Schema: public; Owner: petr_kuril
--

SELECT pg_catalog.setval('public.cars_car_id_seq', 6, true);


--
-- Name: clients_client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: petr_kuril
--

SELECT pg_catalog.setval('public.clients_client_id_seq', 6, true);


--
-- Name: contacts_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: petr_kuril
--

SELECT pg_catalog.setval('public.contacts_contact_id_seq', 7, true);


--
-- Name: contracts_contract_id_seq; Type: SEQUENCE SET; Schema: public; Owner: petr_kuril
--

SELECT pg_catalog.setval('public.contracts_contract_id_seq', 10, true);


--
-- Name: drivers_applications_drivers_applications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: petr_kuril
--

SELECT pg_catalog.setval('public.drivers_applications_drivers_applications_id_seq', 10, true);


--
-- Name: drivers_driver_id_seq; Type: SEQUENCE SET; Schema: public; Owner: petr_kuril
--

SELECT pg_catalog.setval('public.drivers_driver_id_seq', 14, true);


--
-- Name: requisites_requisite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: petr_kuril
--

SELECT pg_catalog.setval('public.requisites_requisite_id_seq', 5, true);


--
-- Name: routes_route_id_seq; Type: SEQUENCE SET; Schema: public; Owner: petr_kuril
--

SELECT pg_catalog.setval('public.routes_route_id_seq', 6, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: petr_kuril
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: applications applications_pkey; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_pkey PRIMARY KEY (application_id);


--
-- Name: blacklist_tokens blacklist_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.blacklist_tokens
    ADD CONSTRAINT blacklist_tokens_pkey PRIMARY KEY (id);


--
-- Name: blacklist_tokens blacklist_tokens_token_key; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.blacklist_tokens
    ADD CONSTRAINT blacklist_tokens_token_key UNIQUE (token);


--
-- Name: cargos cargos_pkey; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.cargos
    ADD CONSTRAINT cargos_pkey PRIMARY KEY (cargo_id);


--
-- Name: cars_applications cars_applications_pkey; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.cars_applications
    ADD CONSTRAINT cars_applications_pkey PRIMARY KEY (cars_applications_id);


--
-- Name: cars cars_pkey; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_pkey PRIMARY KEY (car_id);


--
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (client_id);


--
-- Name: contacts contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_pkey PRIMARY KEY (contact_id);


--
-- Name: contracts contracts_pkey; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.contracts
    ADD CONSTRAINT contracts_pkey PRIMARY KEY (contract_id);


--
-- Name: drivers_applications drivers_applications_pkey; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.drivers_applications
    ADD CONSTRAINT drivers_applications_pkey PRIMARY KEY (drivers_applications_id);


--
-- Name: drivers drivers_pkey; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.drivers
    ADD CONSTRAINT drivers_pkey PRIMARY KEY (driver_id);


--
-- Name: requisites requisites_pkey; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.requisites
    ADD CONSTRAINT requisites_pkey PRIMARY KEY (requisite_id);


--
-- Name: routes routes_pkey; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_pkey PRIMARY KEY (route_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: applications applications_delivery_route_fkey; Type: FK CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_delivery_route_fkey FOREIGN KEY (delivery_route) REFERENCES public.routes(route_id);


--
-- Name: applications applications_receiver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_receiver_id_fkey FOREIGN KEY (receiver_id) REFERENCES public.contacts(contact_id);


--
-- Name: applications applications_shipper_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_shipper_id_fkey FOREIGN KEY (shipper_id) REFERENCES public.contacts(contact_id);


--
-- Name: cargos cargos_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.cargos
    ADD CONSTRAINT cargos_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.applications(application_id);


--
-- Name: cars_applications cars_applications_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.cars_applications
    ADD CONSTRAINT cars_applications_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.applications(application_id);


--
-- Name: cars_applications cars_applications_car_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.cars_applications
    ADD CONSTRAINT cars_applications_car_id_fkey FOREIGN KEY (car_id) REFERENCES public.cars(car_id);


--
-- Name: contracts contracts_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.contracts
    ADD CONSTRAINT contracts_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.applications(application_id);


--
-- Name: contracts contracts_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.contracts
    ADD CONSTRAINT contracts_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(client_id);


--
-- Name: contracts contracts_requisite_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.contracts
    ADD CONSTRAINT contracts_requisite_id_fkey FOREIGN KEY (requisite_id) REFERENCES public.requisites(requisite_id);


--
-- Name: drivers_applications drivers_applications_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.drivers_applications
    ADD CONSTRAINT drivers_applications_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.applications(application_id);


--
-- Name: drivers_applications drivers_applications_driver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: petr_kuril
--

ALTER TABLE ONLY public.drivers_applications
    ADD CONSTRAINT drivers_applications_driver_id_fkey FOREIGN KEY (driver_id) REFERENCES public.drivers(driver_id);


--
-- petr_kurilQL database dump complete
--

