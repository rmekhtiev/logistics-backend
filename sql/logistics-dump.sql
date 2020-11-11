--
-- PostgreSQL database dump
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
-- Name: logistics; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE logistics WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Russian_Russia.1251' LC_CTYPE = 'Russian_Russia.1251';


ALTER DATABASE logistics OWNER TO postgres;

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: applications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.applications (
    application_id integer NOT NULL,
    name character varying(128) NOT NULL,
    conclusion_date date NOT NULL,
    delivery_route integer,
    shipper_id integer,
    receiver_id integer,
    status character varying(9)
);


ALTER TABLE public.applications OWNER TO postgres;

--
-- Name: applications_application_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.applications_application_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.applications_application_id_seq OWNER TO postgres;

--
-- Name: applications_application_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.applications_application_id_seq OWNED BY public.applications.application_id;


--
-- Name: cargos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cargos (
    cargo_id integer NOT NULL,
    nomenclature character varying(64) NOT NULL,
    weight double precision NOT NULL,
    application_id integer
);


ALTER TABLE public.cargos OWNER TO postgres;

--
-- Name: cargos_cargo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cargos_cargo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cargos_cargo_id_seq OWNER TO postgres;

--
-- Name: cargos_cargo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cargos_cargo_id_seq OWNED BY public.cargos.cargo_id;


--
-- Name: cars; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cars (
    car_id integer NOT NULL,
    weight double precision NOT NULL,
    volume double precision NOT NULL,
    model character varying(64) NOT NULL,
    category character varying(1) NOT NULL
);


ALTER TABLE public.cars OWNER TO postgres;

--
-- Name: cars_applications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cars_applications (
    car_id integer,
    application_id integer,
    cars_applications_id integer NOT NULL
);


ALTER TABLE public.cars_applications OWNER TO postgres;

--
-- Name: cars_applications_cars_applications_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
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
-- Name: cars_car_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cars_car_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cars_car_id_seq OWNER TO postgres;

--
-- Name: cars_car_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cars_car_id_seq OWNED BY public.cars.car_id;


--
-- Name: clients; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.clients OWNER TO postgres;

--
-- Name: clients_client_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clients_client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.clients_client_id_seq OWNER TO postgres;

--
-- Name: clients_client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clients_client_id_seq OWNED BY public.clients.client_id;


--
-- Name: contacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contacts (
    contact_id integer NOT NULL,
    first_name character varying(32) NOT NULL,
    last_name character varying(32) NOT NULL,
    middle_name character varying(32),
    "position" character varying(32),
    organization character varying(64),
    phone character varying(11)
);


ALTER TABLE public.contacts OWNER TO postgres;

--
-- Name: contacts_contact_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contacts_contact_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contacts_contact_id_seq OWNER TO postgres;

--
-- Name: contacts_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contacts_contact_id_seq OWNED BY public.contacts.contact_id;


--
-- Name: contracts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contracts (
    contract_id integer NOT NULL,
    conclusion_date date NOT NULL,
    cost numeric(10,2) NOT NULL,
    payment_type character varying(32),
    client_id integer,
    application_id integer
);


ALTER TABLE public.contracts OWNER TO postgres;

--
-- Name: contracts_contract_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contracts_contract_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contracts_contract_id_seq OWNER TO postgres;

--
-- Name: contracts_contract_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contracts_contract_id_seq OWNED BY public.contracts.contract_id;


--
-- Name: drivers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.drivers (
    driver_id integer NOT NULL,
    first_name character varying(32) NOT NULL,
    last_name character varying(32) NOT NULL,
    middle_name character varying(32),
    categories character varying[],
    phone character varying(11)
);


ALTER TABLE public.drivers OWNER TO postgres;

--
-- Name: drivers_applications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.drivers_applications (
    driver_id integer,
    application_id integer,
    drivers_applications_id integer NOT NULL
);


ALTER TABLE public.drivers_applications OWNER TO postgres;

--
-- Name: drivers_applications_drivers_applications_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
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
-- Name: drivers_driver_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.drivers_driver_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.drivers_driver_id_seq OWNER TO postgres;

--
-- Name: drivers_driver_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.drivers_driver_id_seq OWNED BY public.drivers.driver_id;


--
-- Name: requisites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.requisites (
    requisite_id integer NOT NULL,
    bank_name character varying(64) NOT NULL,
    "BIK" character varying(9) NOT NULL,
    "INN" character varying(10) NOT NULL,
    "KPP" character varying(9) NOT NULL,
    "KS" character varying(20) NOT NULL,
    "RS" character varying(20) NOT NULL,
    bank_account character varying(20) NOT NULL,
    contract_id integer
);


ALTER TABLE public.requisites OWNER TO postgres;

--
-- Name: requisites_requisite_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.requisites_requisite_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.requisites_requisite_id_seq OWNER TO postgres;

--
-- Name: requisites_requisite_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.requisites_requisite_id_seq OWNED BY public.requisites.requisite_id;


--
-- Name: routes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.routes (
    route_id integer NOT NULL,
    delivery_address character varying(128) NOT NULL,
    shipping_address character varying(128) NOT NULL,
    distance double precision,
    estimated_time integer
);


ALTER TABLE public.routes OWNER TO postgres;

--
-- Name: routes_route_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.routes_route_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.routes_route_id_seq OWNER TO postgres;

--
-- Name: routes_route_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.routes_route_id_seq OWNED BY public.routes.route_id;


--
-- Name: applications application_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.applications ALTER COLUMN application_id SET DEFAULT nextval('public.applications_application_id_seq'::regclass);


--
-- Name: cargos cargo_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cargos ALTER COLUMN cargo_id SET DEFAULT nextval('public.cargos_cargo_id_seq'::regclass);


--
-- Name: cars car_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars ALTER COLUMN car_id SET DEFAULT nextval('public.cars_car_id_seq'::regclass);


--
-- Name: clients client_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients ALTER COLUMN client_id SET DEFAULT nextval('public.clients_client_id_seq'::regclass);


--
-- Name: contacts contact_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts ALTER COLUMN contact_id SET DEFAULT nextval('public.contacts_contact_id_seq'::regclass);


--
-- Name: contracts contract_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contracts ALTER COLUMN contract_id SET DEFAULT nextval('public.contracts_contract_id_seq'::regclass);


--
-- Name: drivers driver_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.drivers ALTER COLUMN driver_id SET DEFAULT nextval('public.drivers_driver_id_seq'::regclass);


--
-- Name: requisites requisite_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requisites ALTER COLUMN requisite_id SET DEFAULT nextval('public.requisites_requisite_id_seq'::regclass);


--
-- Name: routes route_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.routes ALTER COLUMN route_id SET DEFAULT nextval('public.routes_route_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
46ddf3e7f85a
\.


--
-- Data for Name: applications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.applications (application_id, name, conclusion_date, delivery_route, shipper_id, receiver_id, status) FROM stdin;
1	Доставка чего-то	2020-11-20	6	\N	\N	\N
3	Дилдо (100 штук)	2020-11-30	2	\N	\N	\N
4	Joint запрос	2020-11-25	1	\N	\N	\N
5	Доставка огромной коллекции разноцветных членов на присосках со встроенным вибратором	2020-10-23	3	2	2	active
2	Телевизор	2020-12-12	5	\N	\N	finished
\.


--
-- Data for Name: cargos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cargos (cargo_id, nomenclature, weight, application_id) FROM stdin;
1	Дилдо	156.23	3
2	Joint	0.15	4
3	Телевизор	40	2
4	Холодильник ЗИЛ	60	1
\.


--
-- Data for Name: cars; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cars (car_id, weight, volume, model, category) FROM stdin;
1	3500	25	MAN	D
3	2500	15	FOX	D
4	3500	21	MAN	D
\.


--
-- Data for Name: cars_applications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cars_applications (car_id, application_id, cars_applications_id) FROM stdin;
1	5	1
1	2	2
\.


--
-- Data for Name: clients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clients (client_id, passport_number, passport_series, first_name, last_name, middle_name, email, phone) FROM stdin;
1	4526	588761	Афонт\n	Семендяев	Константинович	afont@gmail.com	79854751892
2	5819	499601	Евстрахий	Полено	Петрович	EfstrahTheLog@mail.ru	79162185692
3	4478	512485	Аббоссали	Мовсисян	Мунарбекович\n	abbossali1976@mail.ru	79856832385
\.


--
-- Data for Name: contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contacts (contact_id, first_name, last_name, middle_name, "position", organization, phone) FROM stdin;
1	Максим	Бобров\n	Петрович	\N	\N	\N
2	Артём\n	Студнев	Викторович\n	\N	\N	\N
\.


--
-- Data for Name: contracts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contracts (contract_id, conclusion_date, cost, payment_type, client_id, application_id) FROM stdin;
\.


--
-- Data for Name: drivers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.drivers (driver_id, first_name, last_name, middle_name, categories, phone) FROM stdin;
8	Пётр	Водило	Азбекович	{'A','B','D'}	79164152615
2	Атманда	Пивницкий	Мурзоевич	{'A','B','D','E','F'}	79857482464
\.


--
-- Data for Name: drivers_applications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.drivers_applications (driver_id, application_id, drivers_applications_id) FROM stdin;
2	5	2
\.


--
-- Data for Name: requisites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.requisites (requisite_id, bank_name, "BIK", "INN", "KPP", "KS", "RS", bank_account, contract_id) FROM stdin;
\.


--
-- Data for Name: routes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.routes (route_id, delivery_address, shipping_address, distance, estimated_time) FROM stdin;
1	asd	adas	\N	\N
2	Шоссе Энтузиастов	Дом Семёна	245	60
3	Дом Семёна	Дом Руслана	8500	240
4	Дом Руслана	РТУ МИРЭА	4500	78
5	Дом Семёна	Подвал МГУПИ	6700	123
6	Откуда-то	Куда-то	\N	\N
\.


--
-- Name: applications_application_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.applications_application_id_seq', 5, true);


--
-- Name: cargos_cargo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cargos_cargo_id_seq', 1, false);


--
-- Name: cars_applications_cars_applications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cars_applications_cars_applications_id_seq', 2, true);


--
-- Name: cars_car_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cars_car_id_seq', 4, true);


--
-- Name: clients_client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clients_client_id_seq', 1, false);


--
-- Name: contacts_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contacts_contact_id_seq', 2, true);


--
-- Name: contracts_contract_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contracts_contract_id_seq', 1, false);


--
-- Name: drivers_applications_drivers_applications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.drivers_applications_drivers_applications_id_seq', 2, true);


--
-- Name: drivers_driver_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.drivers_driver_id_seq', 8, true);


--
-- Name: requisites_requisite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.requisites_requisite_id_seq', 1, false);


--
-- Name: routes_route_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.routes_route_id_seq', 6, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: applications applications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_pkey PRIMARY KEY (application_id);


--
-- Name: cargos cargos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cargos
    ADD CONSTRAINT cargos_pkey PRIMARY KEY (cargo_id);


--
-- Name: cars_applications cars_applications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars_applications
    ADD CONSTRAINT cars_applications_pkey PRIMARY KEY (cars_applications_id);


--
-- Name: cars cars_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_pkey PRIMARY KEY (car_id);


--
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (client_id);


--
-- Name: contacts contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_pkey PRIMARY KEY (contact_id);


--
-- Name: contracts contracts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contracts
    ADD CONSTRAINT contracts_pkey PRIMARY KEY (contract_id);


--
-- Name: drivers_applications drivers_applications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.drivers_applications
    ADD CONSTRAINT drivers_applications_pkey PRIMARY KEY (drivers_applications_id);


--
-- Name: drivers drivers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.drivers
    ADD CONSTRAINT drivers_pkey PRIMARY KEY (driver_id);


--
-- Name: requisites requisites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requisites
    ADD CONSTRAINT requisites_pkey PRIMARY KEY (requisite_id);


--
-- Name: routes routes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_pkey PRIMARY KEY (route_id);


--
-- Name: applications applications_delivery_route_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_delivery_route_fkey FOREIGN KEY (delivery_route) REFERENCES public.routes(route_id);


--
-- Name: applications applications_receiver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_receiver_id_fkey FOREIGN KEY (receiver_id) REFERENCES public.contacts(contact_id);


--
-- Name: applications applications_shipper_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_shipper_id_fkey FOREIGN KEY (shipper_id) REFERENCES public.contacts(contact_id);


--
-- Name: cargos cargos_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cargos
    ADD CONSTRAINT cargos_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.applications(application_id);


--
-- Name: cars_applications cars_applications_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars_applications
    ADD CONSTRAINT cars_applications_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.applications(application_id);


--
-- Name: cars_applications cars_applications_car_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars_applications
    ADD CONSTRAINT cars_applications_car_id_fkey FOREIGN KEY (car_id) REFERENCES public.cars(car_id);


--
-- Name: contracts contracts_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contracts
    ADD CONSTRAINT contracts_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.applications(application_id);


--
-- Name: contracts contracts_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contracts
    ADD CONSTRAINT contracts_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(client_id);


--
-- Name: drivers_applications drivers_applications_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.drivers_applications
    ADD CONSTRAINT drivers_applications_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.applications(application_id);


--
-- Name: drivers_applications drivers_applications_driver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.drivers_applications
    ADD CONSTRAINT drivers_applications_driver_id_fkey FOREIGN KEY (driver_id) REFERENCES public.drivers(driver_id);


--
-- Name: requisites requisites_contract_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requisites
    ADD CONSTRAINT requisites_contract_id_fkey FOREIGN KEY (contract_id) REFERENCES public.contracts(contract_id);


--
-- PostgreSQL database dump complete
--

