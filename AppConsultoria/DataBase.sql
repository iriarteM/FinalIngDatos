CREATE TABLE afiliados (
    user_af            VARCHAR2(30) NOT NULL,
    dni_af             VARCHAR2(8) NOT NULL,
    nombre_af          VARCHAR2(50) NOT NULL,
    rama_militar       VARCHAR2(50) NOT NULL,
    salario_af         NUMBER(10) NOT NULL,
    direc_af           VARCHAR2(80) NOT NULL,
    correo_af          VARCHAR2(80) NOT NULL,
    telef_af           VARCHAR2(9) NOT NULL
);

ALTER TABLE afiliados ADD CONSTRAINT afiliados_pk PRIMARY KEY ( user_af );

CREATE TABLE consultorias (
    id_consul          VARCHAR2(20) NOT NULL,
    num_consul         VARCHAR2(10) NOT NULL,
    tipo_consul        VARCHAR2(80) NOT NULL,
    estado_consul      VARCHAR2(30) NOT NULL,
    fecha_consul       DATE NOT NULL,
    hora_consul        DATE NOT NULL,
    empleados_user_emp VARCHAR2(30) NOT NULL,
    afiliados_user_af  VARCHAR2(30) NOT NULL
);

ALTER TABLE consultorias ADD CONSTRAINT consultorias_pk PRIMARY KEY ( id_consul );

CREATE TABLE contratos (
    id_contrato       VARCHAR2(30) NOT NULL,
    afiliados_user_af VARCHAR2(30) NOT NULL,
    tipo_contrato     VARCHAR2(50) NOT NULL,
    monto_contrato    NUMBER(10) NOT NULL,
    financiamiento    NUMBER(2),
    fecha_contrato    DATE NOT NULL,
    fecha_caducidad   DATE NOT NULL
);

ALTER TABLE contratos ADD CONSTRAINT contratos_pk PRIMARY KEY ( id_contrato );

CREATE TABLE cuentas (
    afiliados_user_af     VARCHAR2(30) NOT NULL,
    contratos_id_contrato VARCHAR2(30) NOT NULL,
    num_cuenta            VARCHAR2(30) NOT NULL,
    monto_cuenta          NUMBER(10) NOT NULL,
    fecha_creacion        DATE NOT NULL,
    num_prestamos         NUMBER(10) NOT NULL,
    mensualidad           NUMBER(10) NOT NULL
);

ALTER TABLE cuentas ADD CONSTRAINT cuentas_pk PRIMARY KEY ( num_cuenta );

CREATE TABLE empleados (
    user_emp    VARCHAR2(30) NOT NULL,
    dni_emp     NUMBER(8) NOT NULL,
    nombre_emp  VARCHAR2(50) NOT NULL,
    salario_emp NUMBER(10) NOT NULL,
    correo_emp  VARCHAR2(80) NOT NULL,
    sexo_emp    VARCHAR2(20) NOT NULL
);

ALTER TABLE empleados ADD CONSTRAINT empleados_pk PRIMARY KEY ( user_emp );

CREATE TABLE familiares (
    afiliados_user_af VARCHAR2(30) NOT NULL,
    dni_fam           NUMBER(8) NOT NULL,
    nombre_fam        VARCHAR2(50) NOT NULL,
    parentesco        VARCHAR2(50) NOT NULL,
    direc_fam         VARCHAR2(80) NOT NULL
);

ALTER TABLE familiares ADD CONSTRAINT familiares_pk PRIMARY KEY ( dni_fam );

CREATE TABLE historial (
    afiliados_user_af VARCHAR2(30) NOT NULL,
    fecha_inicio      DATE NOT NULL,
    fecha_fin         DATE
);

ALTER TABLE historial ADD CONSTRAINT historial_pk PRIMARY KEY ( afiliados_user_af );

ALTER TABLE consultorias
    ADD CONSTRAINT consultorias_afiliados_fk FOREIGN KEY ( afiliados_user_af )
        REFERENCES afiliados ( user_af );

ALTER TABLE consultorias
    ADD CONSTRAINT consultorias_empleados_fk FOREIGN KEY ( empleados_user_emp )
        REFERENCES empleados ( user_emp );

ALTER TABLE contratos
    ADD CONSTRAINT contratos_afiliados_fk FOREIGN KEY ( afiliados_user_af )
        REFERENCES afiliados ( user_af );

ALTER TABLE cuentas
    ADD CONSTRAINT cuentas_afiliados_fk FOREIGN KEY ( afiliados_user_af )
        REFERENCES afiliados ( user_af );

ALTER TABLE cuentas
    ADD CONSTRAINT cuentas_contratos_fk FOREIGN KEY ( contratos_id_contrato )
        REFERENCES contratos ( id_contrato );

ALTER TABLE familiares
    ADD CONSTRAINT familiares_afiliados_fk FOREIGN KEY ( afiliados_user_af )
        REFERENCES afiliados ( user_af );

ALTER TABLE historial
    ADD CONSTRAINT historial_afiliados_fk FOREIGN KEY ( afiliados_user_af )
        REFERENCES afiliados ( user_af );


--EMPLEADOS--
INSERT INTO EMPLEADOS (USER_EMP, DNI_EMP, NOMBRE_EMP, SALARIO_EMP, CORREO_EMP, SEXO_EMP)
VALUES ('empleado1', '12345678', 'Pedro Garc�a', '2000', 'pedro@example.com', 'Masculino');

INSERT INTO EMPLEADOS (USER_EMP, DNI_EMP, NOMBRE_EMP, SALARIO_EMP, CORREO_EMP, SEXO_EMP)
VALUES ('empleado2', '87654321', 'Ana L�pez', '2500', 'ana@example.com', 'Femenino');

INSERT INTO EMPLEADOS (USER_EMP, DNI_EMP, NOMBRE_EMP, SALARIO_EMP, CORREO_EMP, SEXO_EMP)
VALUES ('empleado3', '34253453', 'Steven Ramos', '2000', 'steven@example.com', 'Masculino');

INSERT INTO EMPLEADOS (USER_EMP, DNI_EMP, NOMBRE_EMP, SALARIO_EMP, CORREO_EMP, SEXO_EMP)
VALUES ('empleado4', '78979654', 'Pepe Ramirez', '2500', 'luis@example.com', 'Masculino');

INSERT INTO EMPLEADOS (USER_EMP, DNI_EMP, NOMBRE_EMP, SALARIO_EMP, CORREO_EMP, SEXO_EMP)
VALUES ('empleado5', '98324235','Homero Simp', '4500', 'lionel@example.com', 'Masculino');

INSERT INTO EMPLEADOS (USER_EMP, DNI_EMP, NOMBRE_EMP, SALARIO_EMP, CORREO_EMP, SEXO_EMP)
VALUES ('empleado6', '77788822', 'Carl Johnson', '150000', 'cj@example.com', 'Masculino');


--AFILIADOS--
INSERT INTO AFILIADOS (USER_AF, DNI_AF, NOMBRE_AF, RAMA_MILITAR, SALARIO_AF, DIREC_AF, CORREO_AF, TELEF_AF)
VALUES ('usuario1', '12345678', 'Alan Garcia', 'Ej�rcito', 2500, 'Pal 123', 'juan@example.com', '987654321');

INSERT INTO AFILIADOS (USER_AF, DNI_AF, NOMBRE_AF, RAMA_MILITAR, SALARIO_AF, DIREC_AF, CORREO_AF, TELEF_AF)
VALUES ('usuario2', '87654321', 'Steven Pizarro', 'Fuerza A�rea', 3000, 'Cen 456', 'steven@example.com', '434365543');

INSERT INTO AFILIADOS (USER_AF, DNI_AF, NOMBRE_AF, RAMA_MILITAR, SALARIO_AF, DIREC_AF, CORREO_AF, TELEF_AF)
VALUES ('usuario3', '34435435', 'Javier Fiestas', 'Marina', 4000, 'SaritaCOL', 'javier@example.com', '546543456');

INSERT INTO AFILIADOS (USER_AF, DNI_AF, NOMBRE_AF, RAMA_MILITAR, SALARIO_AF, DIREC_AF, CORREO_AF, TELEF_AF)
VALUES ('usuario4', '78686567', 'Mirko Iriarte', 'Fuerza A�rea', 3000, 'Cen 456', 'mirko@example.com', '645653423');

INSERT INTO AFILIADOS (USER_AF, DNI_AF, NOMBRE_AF, RAMA_MILITAR, SALARIO_AF, DIREC_AF, CORREO_AF, TELEF_AF)
VALUES ('usuario5', '67879766', 'Axel Yabar', 'Marina', 4000, 'Ave 456', 'axel@example.com', '123456789');

INSERT INTO AFILIADOS (USER_AF, DNI_AF, NOMBRE_AF, RAMA_MILITAR, SALARIO_AF, DIREC_AF, CORREO_AF, TELEF_AF)
VALUES ('1', '1', 'Admin', 'Policia', 5000, 'Street', 'admin@example.com', '123456789');


--FAMILIARES--
INSERT INTO FAMILIARES (AFILIADOS_USER_AF, DNI_FAM, NOMBRE_FAM, PARENTESCO, DIREC_FAM)
VALUES ('usuario1', '11111111', 'Luisa P�rez', 'Hermana', 'Calle 789');

INSERT INTO FAMILIARES (AFILIADOS_USER_AF, DNI_FAM, NOMBRE_FAM, PARENTESCO, DIREC_FAM)
VALUES ('usuario2', '22222222', 'usuario1','Carlos G�mez', 'Hermano', 'Avenida123');

INSERT INTO FAMILIARES (AFILIADOS_USER_AF, DNI_FAM, NOMBRE_FAM, PARENTESCO, DIREC_FAM)
VALUES ('usuario3', '33333333', 'Steven Iriarte', 'Hermano', 'Avenida 153');

INSERT INTO FAMILIARES (AFILIADOS_USER_AF, DNI_FAM, NOMBRE_FAM, PARENTESCO, DIREC_FAM)
VALUES ('usuario4', '44444444', 'Axel Fiestas', 'Hermano', 'Avenida 12453');

INSERT INTO FAMILIARES (AFILIADOS_USER_AF, DNI_FAM, NOMBRE_FAM, PARENTESCO, DIREC_FAM)
VALUES ('usuario5', '55555555', 'Cesar Rosales', 'Hermano', 'Avenida 13243');


--HISTORIAL--
INSERT INTO HISTORIAL (AFILIADOS_USER_AF, FECHA_INICIO, FECHA_FIN)
VALUES ('usuario1', TO_DATE('01-01-2022', 'DD-MM-YYYY'), TO_DATE('31-05-2023', 'DD-MM-YYYY'));

INSERT INTO HISTORIAL (AFILIADOS_USER_AF, FECHA_INICIO, FECHA_FIN)
VALUES ('usuario2', TO_DATE('02-06-2022', 'DD-MM-YYYY'), NULL);

INSERT INTO HISTORIAL (AFILIADOS_USER_AF, FECHA_INICIO, FECHA_FIN)
VALUES ('usuario3', TO_DATE('03-06-2022', 'DD-MM-YYYY'), NULL);

INSERT INTO HISTORIAL (AFILIADOS_USER_AF, FECHA_INICIO, FECHA_FIN)
VALUES ('usuario4', TO_DATE('04-06-2022', 'DD-MM-YYYY'), TO_DATE('26-05-2023', 'DD-MM-YYYY'));

INSERT INTO HISTORIAL (AFILIADOS_USER_AF, FECHA_INICIO, FECHA_FIN)
VALUES ('usuario5', TO_DATE('05-06-2022', 'DD-MM-YYYY'), NULL);


--CONSULTORIAS--
INSERT INTO CONSULTORIAS (ID_CONSUL, NUM_CONSUL, TIPO_CONSUL, ESTADO_CONSUL, FECHA_CONSUL, EMPLEADOS_USER_EMP, AFILIADOS_USER_AF)
VALUES ('C1', '1', 'Finanzas', 'Pendiente', TO_DATE('30-07-2023', 'DD-MM-YYYY'), 'empleado1', 'usuario1');

INSERT INTO CONSULTORIAS (ID_CONSUL, NUM_CONSUL, TIPO_CONSUL, ESTADO_CONSUL, FECHA_CONSUL, EMPLEADOS_USER_EMP, AFILIADOS_USER_AF)
VALUES ('C2', '1', 'Cuentas', 'Pendiente', TO_DATE('30-07-2023', 'DD-MM-YYYY'), 'empleado2', 'usuario2');

INSERT INTO CONSULTORIAS (ID_CONSUL, NUM_CONSUL, TIPO_CONSUL, ESTADO_CONSUL, FECHA_CONSUL, EMPLEADOS_USER_EMP, AFILIADOS_USER_AF)
VALUES ('C3', '1', 'Contratos', 'Completada', TO_DATE('30-07-2023', 'DD-MM-YYYY'), 'empleado3', 'usuario3');

INSERT INTO CONSULTORIAS (ID_CONSUL, NUM_CONSUL, TIPO_CONSUL, ESTADO_CONSUL, FECHA_CONSUL, EMPLEADOS_USER_EMP, AFILIADOS_USER_AF)
VALUES ('C4', '1', 'Finanzas', 'Completada', TO_DATE('30-07-2023', 'DD-MM-YYYY'), 'empleado4', 'usuario4');

INSERT INTO CONSULTORIAS (ID_CONSUL, NUM_CONSUL, TIPO_CONSUL, ESTADO_CONSUL, FECHA_CONSUL, EMPLEADOS_USER_EMP, AFILIADOS_USER_AF)
VALUES ('C5', '1', 'Otros', 'Pendiente', TO_DATE('30-07-2023', 'DD-MM-YYYY'), 'empleado5', 'usuario5');

INSERT INTO CONSULTORIAS (ID_CONSUL, NUM_CONSUL, TIPO_CONSUL, ESTADO_CONSUL, FECHA_CONSUL, EMPLEADOS_USER_EMP, AFILIADOS_USER_AF)
VALUES ('C6', '1', 'Contratos', 'Pendiente', TO_DATE('30-07-2023', 'DD-MM-YYYY'), 'empleado1', '1');

INSERT INTO CONSULTORIAS (ID_CONSUL, NUM_CONSUL, TIPO_CONSUL, ESTADO_CONSUL, FECHA_CONSUL, EMPLEADOS_USER_EMP, AFILIADOS_USER_AF)
VALUES ('C7', '2', 'Cuentas', 'Pendiente', TO_DATE('30-07-2023', 'DD-MM-YYYY'), 'empleado2', '1');


--CONTRATOS--
INSERT INTO CONTRATOS (ID_CONTRATO, AFILIADOS_USER_AF, TIPO_CONTRATO, MONTO_CONTRATO, FINANCIAMIENTO, FECHA_CONTRATO, FECHA_CADUCIDAD)
VALUES ('CONTRATO1', 'usuario1', 'Pr�stamo', 5000, 12, TO_DATE('01-06-2023', 'DD-MM-YYYY'), TO_DATE('01-12-2023', 'DD-MM-YYYY'));

INSERT INTO CONTRATOS (ID_CONTRATO, AFILIADOS_USER_AF, TIPO_CONTRATO, MONTO_CONTRATO, FINANCIAMIENTO, FECHA_CONTRATO, FECHA_CADUCIDAD)
VALUES ('CONTRATO2', 'usuario2', 'Auxilio', 10000, NULL, TO_DATE('02-06-2023', 'DD-MM-YYYY'), TO_DATE('02-06-2024', 'DD-MM-YYYY'));

INSERT INTO CONTRATOS (ID_CONTRATO, AFILIADOS_USER_AF, TIPO_CONTRATO, MONTO_CONTRATO, FINANCIAMIENTO, FECHA_CONTRATO, FECHA_CADUCIDAD)
VALUES ('CONTRATO3', 'usuario3', 'Auxilio', 15000, NULL, TO_DATE('03-06-2023', 'DD-MM-YYYY'), TO_DATE('12-08-2024', 'DD-MM-YYYY'));

INSERT INTO CONTRATOS (ID_CONTRATO, AFILIADOS_USER_AF, TIPO_CONTRATO, MONTO_CONTRATO, FINANCIAMIENTO, FECHA_CONTRATO, FECHA_CADUCIDAD)
VALUES ('CONTRATO4', 'usuario4', 'Pr�stamo', 30000, 48, TO_DATE('04-06-2023', 'DD-MM-YYYY'), TO_DATE('25-06-2024', 'DD-MM-YYYY'));

INSERT INTO CONTRATOS (ID_CONTRATO, AFILIADOS_USER_AF, TIPO_CONTRATO, MONTO_CONTRATO, FINANCIAMIENTO, FECHA_CONTRATO, FECHA_CADUCIDAD)
VALUES ('CONTRATO5', 'usuario5', 'Pr�stamo', 12000, 18, TO_DATE('05-06-2023', 'DD-MM-YYYY'), TO_DATE('15-07-2024', 'DD-MM-YYYY'));


--CUENTAS--
INSERT INTO CUENTAS (AFILIADOS_USER_AF, CONTRATOS_ID_CONTRATO, NUM_CUENTA, MONTO_CUENTA, FECHA_CREACION, NUM_PRESTAMOS, MENSUALIDAD)
VALUES ('usuario1', 'CONTRATO1', 'CUENTA1', 5000, TO_DATE('01-06-2023', 'DD-MM-YYYY'), 2, 200);

INSERT INTO CUENTAS (AFILIADOS_USER_AF, CONTRATOS_ID_CONTRATO, NUM_CUENTA, MONTO_CUENTA, FECHA_CREACION, NUM_PRESTAMOS, MENSUALIDAD)
VALUES ('usuario2', 'CONTRATO2', 'CUENTA2', 10000, TO_DATE('02-06-2023', 'DD-MM-YYYY'), 1, 300);

INSERT INTO CUENTAS (AFILIADOS_USER_AF, CONTRATOS_ID_CONTRATO, NUM_CUENTA, MONTO_CUENTA, FECHA_CREACION, NUM_PRESTAMOS, MENSUALIDAD)
VALUES ('usuario3', 'CONTRATO3', 'CUENTA3', 10000, TO_DATE('03-06-2023', 'DD-MM-YYYY'), 1, 400);

INSERT INTO CUENTAS (AFILIADOS_USER_AF, CONTRATOS_ID_CONTRATO, NUM_CUENTA, MONTO_CUENTA, FECHA_CREACION, NUM_PRESTAMOS, MENSUALIDAD)
VALUES ('usuario4', 'CONTRATO4', 'CUENTA4', 10000, TO_DATE('04-06-2023', 'DD-MM-YYYY'), 1, 500);

INSERT INTO CUENTAS (AFILIADOS_USER_AF, CONTRATOS_ID_CONTRATO, NUM_CUENTA, MONTO_CUENTA, FECHA_CREACION, NUM_PRESTAMOS, MENSUALIDAD)
VALUES ('usuario5', 'CONTRATO5', 'CUENTA5', 10000, TO_DATE('05-06-2023', 'DD-MM-YYYY'), 1, 600);





--------------PROCEDIMIENTOS ALMACENADOS--------------

--Insertar una nueva consulta
CREATE OR REPLACE PROCEDURE INSERTAR_CONSULTA(
    p_id_consul IN VARCHAR2,
    p_num_consul IN VARCHAR2,
    p_tipo_consul IN VARCHAR2,
    p_estado_consul IN VARCHAR2,
    p_fecha_consul IN DATE,
    p_empleado_user_emp IN VARCHAR2,
    p_afiliado_user_af IN VARCHAR2
) AS
BEGIN
    INSERT INTO consultorias (
        id_consul,
        num_consul,
        tipo_consul,
        estado_consul,
        fecha_consul,
        empleados_user_emp,
        afiliados_user_af
    ) VALUES (
        p_id_consul,
        p_num_consul,
        p_tipo_consul,
        p_estado_consul,
        p_fecha_consul,
        p_empleado_user_emp,
        p_afiliado_user_af
    );
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
    ROLLBACK;
    RAISE;
END;
/


--Actualizar (Editar) una consulta
CREATE OR REPLACE PROCEDURE ACTUALIZAR_CONSULTA(
    p_num_consul IN VARCHAR2,
    p_tipo_consul IN VARCHAR2,
    p_fecha_consul IN DATE,
    p_empleado_user_emp IN VARCHAR2,
    p_afiliado_user_af IN VARCHAR2
) AS
BEGIN
    UPDATE CONSULTORIAS
    SET TIPO_CONSUL = P_TIPO_CONSUL,
        FECHA_CONSUL = P_FECHA_CONSUL,
        EMPLEADOS_USER_EMP = P_EMPLEADO_USER_EMP
    WHERE NUM_CONSUL = P_NUM_CONSUL
      AND AFILIADOS_USER_AF = P_AFILIADO_USER_AF;
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
    ROLLBACK;
    RAISE;
END;
/


-- Eliminar una consulta
CREATE OR REPLACE PROCEDURE ELIMINAR_CONSULTA(
    p_num_consul IN VARCHAR2,
    p_afiliado_user_af IN VARCHAR2
) AS
BEGIN
    DELETE FROM consultorias
    WHERE num_consul = p_num_consul
      AND afiliados_user_af = p_afiliado_user_af;
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/


-- Insertar un nuevo familiar
CREATE OR REPLACE PROCEDURE INSERTAR_FAMILIAR(
    p_afiliados_user_af IN VARCHAR2,
    p_dni_fam IN VARCHAR2,
    p_nombre_fam IN VARCHAR2,
    p_parentesco IN VARCHAR2,
    p_direc_fam IN VARCHAR2
) AS
BEGIN
    INSERT INTO familiares (
        afiliados_user_af,
        dni_fam,
        nombre_fam,
        parentesco,
        direc_fam
    ) VALUES (
        p_afiliados_user_af,
        p_dni_fam,
        p_nombre_fam,
        p_parentesco,
        p_direc_fam
    );
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/


-- Actualizar (editar) un familiar
CREATE OR REPLACE PROCEDURE ACTUALIZAR_FAMILIAR(
    p_afiliados_user_af IN VARCHAR2,
    p_dni_fam IN NUMBER,
    p_nombre_fam IN VARCHAR2,
    p_parentesco IN VARCHAR2,
    p_direc_fam IN VARCHAR2
    
) AS
BEGIN
    UPDATE familiares
    SET nombre_fam = p_nombre_fam,
        parentesco = p_parentesco,
        direc_fam = p_direc_fam
    WHERE dni_fam = p_dni_fam
      AND afiliados_user_af = p_afiliados_user_af;
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/


-- Eliminar un familiar
CREATE OR REPLACE PROCEDURE ELIMINAR_FAMILIAR(
    p_dni_fam IN NUMBER,
    p_afiliados_user_af IN VARCHAR2
) AS
BEGIN
    DELETE FROM familiares
    WHERE dni_fam = p_dni_fam
      AND afiliados_user_af = p_afiliados_user_af;
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/


-- Registar un nuevo afiliado
CREATE OR REPLACE PROCEDURE REGISTRO(
    p_USER_AF IN VARCHAR2,
    p_DNI_AF IN VARCHAR2,
    p_NOMBRE_AF IN VARCHAR2,
    p_RAMA_MILITAR IN VARCHAR2,
    p_SALARIO_AF IN NUMBER,
    p_DIREC_AF IN VARCHAR2,
    p_CORREO_AF IN VARCHAR2,
    p_TELEF_AF IN VARCHAR2
) AS
BEGIN
    INSERT INTO AFILIADOS (
        USER_AF, 
        DNI_AF, 
        NOMBRE_AF, 
        RAMA_MILITAR, 
        SALARIO_AF, 
        DIREC_AF, 
        CORREO_AF, 
        TELEF_AF
    ) VALUES (
        p_USER_AF,
        p_DNI_AF,
        p_NOMBRE_AF,
        p_RAMA_MILITAR,
        p_SALARIO_AF,
        p_DIREC_AF,
        p_CORREO_AF,
        p_TELEF_AF
    );
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/


--------TRIGGERS--------

-- Salario del afiliado no sea negativo
CREATE OR REPLACE TRIGGER TRG_AFILIADO_SALARIO
BEFORE INSERT OR UPDATE ON AFILIADOS
FOR EACH ROW
BEGIN
    IF :NEW.SALARIO_AF < 0 THEN
        raise_application_error(-20001, 'El salario del afiliado no puede ser negativo.');
    END IF;
END;
/


-- Trigger si se elimina un afiliado, tambien sus familiares
CREATE OR REPLACE TRIGGER TRG_ELIMINAR_AFILIADO_CASCADA
AFTER DELETE ON AFILIADOS
FOR EACH ROW
BEGIN
    DELETE FROM FAMILIARES
    WHERE AFILIADOS_USER_AF = :OLD.USER_AF;
    COMMIT;
END;
/


-- Longitud del dni igual a 8
CREATE OR REPLACE TRIGGER TRG_VALIDAR_LONGITUD_DNI
BEFORE INSERT OR UPDATE ON AFILIADOS
FOR EACH ROW
BEGIN
    IF LENGTH(:NEW.DNI_AF) <> 8 THEN
        raise_application_error(-20002, 'El DNI debe tener exactamente 8 d�gitos.');
    END IF;
END;
/


-- Longitud del telefono igual a 9
CREATE OR REPLACE TRIGGER TRG_VALIDAR_LONGITUD_TELEFONO
BEFORE INSERT OR UPDATE ON AFILIADOS
FOR EACH ROW
BEGIN
    IF LENGTH(:NEW.TELEF_AF) <> 9 THEN
        raise_application_error(-20003, 'El n�mero de tel�fono debe tener exactamente 9 d�gitos.');
    END IF;
END;
/


-- Evitar que se inserte un afiliado nuevo con un DNI repetido
CREATE OR REPLACE TRIGGER TRG_EVITAR_DNI_DUPLICADO
BEFORE INSERT ON AFILIADOS
FOR EACH ROW
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM AFILIADOS
    WHERE DNI_AF = :NEW.DNI_AF;

    IF v_count > 0 THEN
        raise_application_error(-20009, 'Ya existe un afiliado con el mismo n�mero de DNI.');
    END IF;
END;
/


-- Trigger para no eliminar afiliados con consultas pendientes
CREATE OR REPLACE TRIGGER TRG_EVITAR_ELIMINAR_AFILIADO_CON_CONSULTAS
BEFORE DELETE ON AFILIADOS
FOR EACH ROW
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM CONSULTORIAS
    WHERE AFILIADOS_USER_AF = :OLD.USER_AF AND ESTADO_CONSUL = 'Pendiente';

    IF v_count > 0 THEN
        raise_application_error(-20007, 'No se puede eliminar el afiliado porque tiene consultas pendientes.');
    END IF;
END;
/


-- Trigger para evitar que se inserten fechas con dias pasados
CREATE OR REPLACE TRIGGER TRG_EVITAR_INSERTAR_FECHA_PASADA
BEFORE INSERT ON CONSULTORIAS
FOR EACH ROW
BEGIN
    IF :NEW.FECHA_CONSUL < SYSDATE-1 THEN
        raise_application_error(-20010, 'No se puede insertar una consulta con fecha en el pasado.');
    END IF;
END;
/


-- Trigger para asegurar que solo se puedan insertar consultas para afiliados existentes
CREATE OR REPLACE TRIGGER TRG_VERIFICAR_AFILIADO_EXISTENTE
BEFORE INSERT ON CONSULTORIAS
FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM AFILIADOS
        WHERE USER_AF = :NEW.AFILIADOS_USER_AF
    )
    THEN
        raise_application_error(-20013, 'El afiliado no existe en la base de datos.');
    END IF;
END;
/
