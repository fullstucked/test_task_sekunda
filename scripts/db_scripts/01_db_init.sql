CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

------------------------------------------------------------
-- TABLE: facility
------------------------------------------------------------
CREATE TABLE facility (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    address VARCHAR(255) NOT NULL,
    lat VARCHAR,
    lon VARCHAR
);

CREATE INDEX ix_facility_address ON facility (address);

------------------------------------------------------------
-- TABLE: business_type
------------------------------------------------------------
CREATE TABLE business_type (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    parent_id UUID REFERENCES business_type(id) ON DELETE CASCADE,
    CONSTRAINT uq_business_type_parent_name UNIQUE (parent_id, name)
);

CREATE INDEX ix_business_type_parent ON business_type (parent_id);
CREATE INDEX ix_business_type_name ON business_type (name);

------------------------------------------------------------
-- TABLE: business_type_closure
------------------------------------------------------------
CREATE TABLE business_type_closure (
    ancestor_id UUID NOT NULL REFERENCES business_type(id) ON DELETE CASCADE,
    descendant_id UUID NOT NULL REFERENCES business_type(id) ON DELETE CASCADE,
    depth INTEGER NOT NULL,
    PRIMARY KEY (ancestor_id, descendant_id)
);

CREATE INDEX ix_btc_ancestor ON business_type_closure (ancestor_id);
CREATE INDEX ix_btc_descendant ON business_type_closure (descendant_id);

------------------------------------------------------------
-- TABLE: organization
------------------------------------------------------------
CREATE TABLE organization (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    facility_id UUID NOT NULL REFERENCES facility(id) ON DELETE CASCADE
);

CREATE INDEX ix_organization_name ON organization (name);
CREATE INDEX ix_organization_facility ON organization (facility_id);

------------------------------------------------------------
-- TABLE: phone_table
------------------------------------------------------------
CREATE TABLE phone_table (
    phone_number VARCHAR(50) UNIQUE NOT NULL,
    org_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE
);

CREATE INDEX ix_phone_org ON phone_table (org_id);

------------------------------------------------------------
-- TABLE: organization_business_type
------------------------------------------------------------
CREATE TABLE organization_business_type (
    organization_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    business_type_id UUID NOT NULL REFERENCES business_type(id) ON DELETE CASCADE,
    PRIMARY KEY (organization_id, business_type_id)
);

CREATE INDEX ix_obt_org ON organization_business_type (organization_id);
CREATE INDEX ix_obt_bt ON organization_business_type (business_type_id);

------------------------------------------------------------
-- SAMPLE DATA
------------------------------------------------------------

-------------------------
-- facility (5 rows)
-------------------------
INSERT INTO facility (id, address, lat, lon) VALUES
    ('11111111-1111-1111-1111-111111111111', 'г. Москва, пр-т Мира 10', '55.790001', '37.630001'),
    ('22222222-2222-2222-2222-222222222222', 'г. Москва, ул. Арбат 25', '55.752201', '37.592301'),
    ('33333333-3333-3333-3333-333333333333', 'г. Казань, ул. Баумана 5', '55.796001', '49.106001'),
    ('44444444-4444-4444-4444-444444444444', 'г. Самара, ул. Московское шоссе 120', '53.195001', '50.101001'),
    ('55555555-5555-5555-5555-555555555555', 'г. Пермь, ул. Комсомольский пр-т 30', '58.010001', '56.229001');

-------------------------
-- business_type (tree, 7 rows)
-------------------------
-- Root categories
INSERT INTO business_type (id, name, parent_id) VALUES
    ('aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 'Розничная торговля', NULL),
    ('aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2', 'Услуги', NULL);

-- Children of Розничная торговля
INSERT INTO business_type (id, name, parent_id) VALUES
    ('bbbbbbb1-bbbb-bbbb-bbbb-bbbbbbbbbbb1', 'Продукты', 'aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1'),
    ('bbbbbbb2-bbbb-bbbb-bbbb-bbbbbbbbbbb2', 'Электроника', 'aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1'),
    ('bbbbbbb3-bbbb-bbbb-bbbb-bbbbbbbbbbb3', 'Одежда', 'aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1');

-- Children of Услуги
INSERT INTO business_type (id, name, parent_id) VALUES
    ('ccccccc1-cccc-cccc-cccc-ccccccccccc1', 'Логистика', 'aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2'),
    ('ccccccc2-cccc-cccc-cccc-ccccccccccc2', 'Ремонт техники', 'aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2');

-------------------------
-- business_type_closure
-- (simple closure for the above tree)
-------------------------
INSERT INTO business_type_closure (ancestor_id, descendant_id, depth) VALUES
    -- Розничная торговля
    ('aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 'aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 0),
    ('aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 'bbbbbbb1-bbbb-bbbb-bbbb-bbbbbbbbbbb1', 1),
    ('aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 'bbbbbbb2-bbbb-bbbb-bbbb-bbbbbbbbbbb2', 1),
    ('aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 'bbbbbbb3-bbbb-bbbb-bbbb-bbbbbbbbbbb3', 1),

    ('bbbbbbb1-bbbb-bbbb-bbbb-bbbbbbbbbbb1', 'bbbbbbb1-bbbb-bbbb-bbbb-bbbbbbbbbbb1', 0),
    ('bbbbbbb2-bbbb-bbbb-bbbb-bbbbbbbbbbb2', 'bbbbbbb2-bbbb-bbbb-bbbb-bbbbbbbbbbb2', 0),
    ('bbbbbbb3-bbbb-bbbb-bbbb-bbbbbbbbbbb3', 'bbbbbbb3-bbbb-bbbb-bbbb-bbbbbbbbbbb3', 0),

    -- Услуги
    ('aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2', 'aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2', 0),
    ('aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2', 'ccccccc1-cccc-cccc-cccc-ccccccccccc1', 1),
    ('aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2', 'ccccccc2-cccc-cccc-cccc-ccccccccccc2', 1),

    ('ccccccc1-cccc-cccc-cccc-ccccccccccc1', 'ccccccc1-cccc-cccc-cccc-ccccccccccc1', 0),
    ('ccccccc2-cccc-cccc-cccc-ccccccccccc2', 'ccccccc2-cccc-cccc-cccc-ccccccccccc2', 0);

-------------------------
-- organization (5 rows)
-- несколько организаций в одном facility (1111...)
-------------------------
INSERT INTO organization (id, name, facility_id) VALUES
    ('99999999-1111-1111-1111-111111111111', 'ООО "СеверТорг"', '11111111-1111-1111-1111-111111111111'),
    ('99999999-2222-2222-2222-222222222222', 'ЗАО "ВекторМаркет"', '11111111-1111-1111-1111-111111111111'),
    ('99999999-3333-3333-3333-333333333333', 'ИП "ЭлектроДом"', '22222222-2222-2222-2222-222222222222'),
    ('99999999-4444-4444-4444-444444444444', 'ООО "ГородСтиль"', '33333333-3333-3333-3333-333333333333'),
    ('99999999-5555-5555-5555-555555555555', 'ООО "ТехСервис+"', '44444444-4444-4444-4444-444444444444');

-------------------------
-- phone_table (>=5 rows, some orgs with 2+ phones)
-------------------------
INSERT INTO phone_table ( phone_number, org_id) VALUES
    ( '+7-495-100-20-30', '99999999-1111-1111-1111-111111111111'),
    ( '+7-495-100-20-31', '99999999-1111-1111-1111-111111111111'),

    ( '+7-495-200-30-40', '99999999-2222-2222-2222-222222222222'),
    ( '+7-495-200-30-41', '99999999-2222-2222-2222-222222222222'),

    ( '+7-495-300-40-50', '99999999-3333-3333-3333-333333333333'),
    ( '+7-843-400-50-60', '99999999-4444-4444-4444-444444444444'),
    ( '+7-846-500-60-70', '99999999-5555-5555-5555-555555555555');

-------------------------
-- organization_business_type (links)
-------------------------
INSERT INTO organization_business_type (organization_id, business_type_id) VALUES
    -- СеверТорг: продукты + логистика
    ('99999999-1111-1111-1111-111111111111', 'bbbbbbb1-bbbb-bbbb-bbbb-bbbbbbbbbbb1'),
    ('99999999-1111-1111-1111-111111111111', 'ccccccc1-cccc-cccc-cccc-ccccccccccc1'),

    -- ВекторМаркет: продукты + одежда
    ('99999999-2222-2222-2222-222222222222', 'bbbbbbb1-bbbb-bbbb-bbbb-bbbbbbbbbbb1'),
    ('99999999-2222-2222-2222-222222222222', 'bbbbbbb3-bbbb-bbbb-bbbb-bbbbbbbbbbb3'),

    -- ЭлектроДом: электроника + ремонт техники
    ('99999999-3333-3333-3333-333333333333', 'bbbbbbb2-bbbb-bbbb-bbbb-bbbbbbbbbbb2'),
    ('99999999-3333-3333-3333-333333333333', 'ccccccc2-cccc-cccc-cccc-ccccccccccc2'),

    -- ГородСтиль: одежда
    ('99999999-4444-4444-4444-444444444444', 'bbbbbbb3-bbbb-bbbb-bbbb-bbbbbbbbbbb3'),

    -- ТехСервис+: ремонт техники + логистика
    ('99999999-5555-5555-5555-555555555555', 'ccccccc2-cccc-cccc-cccc-ccccccccccc2'),
    ('99999999-5555-5555-5555-555555555555', 'ccccccc1-cccc-cccc-cccc-ccccccccccc1');
