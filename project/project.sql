


DROP TABLE IF EXISTS "PROSOPIKO";
CREATE TABLE IF NOT EXISTS "PROSOPIKO" (
	"kodikos" integer NOT NULL,
	"onoma" TEXT NOT NULL,
	"eponimo" TEXT NOT NULL,
	"tilefono"     INTEGER NOT NULL,
	"imerominia_proslipsis" TEXT NOT NULL,
	"filo" TEXT NOT NULL,
	PRIMARY KEY ("kodikos" AUTOINCREMENT)	
);

DROP TABLE IF EXISTS "GRAMMATEAS";
CREATE TABLE IF NOT EXISTS "GRAMMATEAS" (
	"kodikos" integer NOT NULL,
	"misthos" REAL NOT NULL,
	PRIMARY KEY ("kodikos"),
	FOREIGN KEY("kodikos") REFERENCES "PROSOPIKO"("kodikos") ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS "PROPONITIS";
CREATE TABLE IF NOT EXISTS "PROPONITIS" (
	"kodikos" integer NOT NULL,
	"amoibi_mathimatos" REAL NOT NULL DEFAULT 10,
	"kostos_mathimatos" REAL NOT NULL DEFAULT 20,
	PRIMARY KEY("kodikos"),
	FOREIGN KEY("kodikos") REFERENCES "PROSOPIKO"("kodikos") ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS "SINTIRITIS";
CREATE TABLE IF NOT EXISTS "SINTIRITIS" (
	"kodikos" integer NOT NULL,
	"misthos" REAL NOT NULL,
	PRIMARY KEY ("kodikos"),
	FOREIGN KEY("kodikos") REFERENCES "PROSOPIKO"("kodikos") ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS "MATHIMA";
CREATE TABLE IF NOT EXISTS "MATHIMA"(
	"epipedo" TEXT NOT NULL,
	"ores_ana_ebdomada" integer NOT NULL,
	PRIMARY KEY ("epipedo"),
	CONSTRAINT "KATIGORIA_epipedo" CHECK ("epipedo" IN("ΑΡΧΑΡΙΟΙ","ΜΕΤΡΙΟΙ","ΠΡΟΧΩΡΗΜΕΝΟΙ"))
);

DROP TABLE IF EXISTS "DIDASKALIA";
CREATE TABLE IF NOT EXISTS "DIDASKALIA" (
	"epipedo" TEXT NOT NULL,
	"etos" TEXT NOT NULL,
	"noumero" integer NOT NULL,
	"miniaio_kostos" integer NOT NULL,
	"ilikiako_euros" text NOT NULL,
	PRIMARY KEY ("epipedo","etos","noumero"),
	FOREIGN KEY ("epipedo") REFERENCES "MATHIMA"("epipedo") ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS "PRAGMATOPOIEI";
CREATE TABLE IF NOT EXISTS "PRAGMATOPOIEI" (
	"kodikos_prop" integer NOT NULL,
	"epipedo_did" TEXT NOT NULL,
	"etos_did" TEXT NOT NULL,
	"noumero_did" integer NOT NULL,
	"ora" TEXT NOT NULL,
	"mera" TEXT NOT NULL,
	PRIMARY KEY("kodikos_prop","epipedo_did","etos_did","noumero_did","ora","mera"),
	FOREIGN KEY("epipedo_did","etos_did","noumero_did") REFERENCES "DIDASKALIA" ("epipedo","etos","noumero") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("kodikos_prop") REFERENCES "PROPONITIS"("kodikos") ON DELETE SET NULL ON UPDATE CASCADE,
	CONSTRAINT "PRAGMATOPOIEI_mera"CHECK("mera" IN("ΔΕΥΤΕΡΑ","ΤΡΙΤΗ","ΤΕΤΑΡΤΗ","ΠΕΜΠΤΗ","ΠΑΡΑΣΚΕΥΗ","ΣΑΒΒΑΤΟ","ΚΥΡΙΑΚΗ")),
	CONSTRAINT "PRAGMATOPOIEI_ora" CHECK("ora" LIKE '__:__-__:__')  
);
 	

DROP TABLE IF EXISTS "PROPONITIS_ORARIO";
CREATE TABLE IF NOT EXISTS "PROPONITIS_ORARIO" (
	"kodikos_prop" integer NOT NULL,
	"ora" TEXT ,
	"mera" TEXT,
	PRIMARY KEY("kodikos_prop","ora","mera"),
	FOREIGN KEY("kodikos_prop") REFERENCES "PROPONITIS"("kodikos") ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT "PROPONITIS_ORARIO_ora" CHECK("ora" LIKE '__:__-__:__'),
	CONSTRAINT "PROPONITIS_ORARIO_mera"CHECK("mera" IN("ΔΕΥΤΕΡΑ","ΤΡΙΤΗ","ΤΕΤΑΡΤΗ","ΠΕΜΠΤΗ","ΠΑΡΑΣΚΕΥΗ","ΣΑΒΒΑΤΟ","ΚΥΡΙΑΚΗ"))
);

DROP TABLE IF EXISTS "GIPEDO";
CREATE TABLE IF NOT EXISTS "GIPEDO" (
	"arithmos_gipedou" integer NOT NULL,
	"eidos_gipedou" TEXT NOT NULL,
	"kodikos_sintiriti" integer DEFAULT null,
	"dieuthinsi" TEXT NOT NULL,
	"kostos_aneks_kratisis" REAL NOT NULL DEFAULT 10,
	PRIMARY KEY("arithmos_gipedou" AUTOINCREMENT),
	FOREIGN KEY("kodikos_sintiriti") REFERENCES "SINTIRITIS"("kodikos") ON DELETE SET NULL ON UPDATE CASCADE,
	CONSTRAINT "GIPEDO_eidos_gipedou" CHECK("eidos_gipedou" IN("ΣΚΛΗΡΟ","ΧΩΜΑΤΙΝΟ","ΜΟΚΕΤΑ","ΓΡΑΣΙΔΙ","ΚΛΕΙΣΤΟ"))
);

DROP TABLE IF EXISTS "KRATISI";
CREATE TABLE IF NOT EXISTS "KRATISI" (
	"kodikos" integer NOT NULL,
	"imerominia" TEXT NOT NULL,
	"ora" TEXT NOT NULL,
	"anablithike" INTEGER DEFAULT 0,
	"arithmos_gipedou" integer NOT NULL,
	PRIMARY KEY("kodikos" AUTOINCREMENT),
	FOREIGN KEY ("arithmos_gipedou") REFERENCES "GIPEDO"("arithmos_gipedou") ON DELETE RESTRICT ON UPDATE CASCADE,
	CONSTRAINT "KRATISI_anablithike" CHECK( "anablithike" IN(0,1) )
);
	
DROP TABLE IF EXISTS "DIMIOURGEI";
CREATE TABLE IF NOT EXISTS "DIMIOURGEI" (
	"epipedo" TEXT NOT NULL,	
	"etos" TEXT NOT NULL,
	"noumero_did" integer NOT NULL,
	"kodikos_krat" integer NOT NULL,
	PRIMARY KEY("epipedo","etos","noumero_did","kodikos_krat"),
	FOREIGN KEY("epipedo","etos","noumero_did") REFERENCES "DIDASKALIA"("epipedo","etos","noumero") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("kodikos_krat") REFERENCES "KRATISI"("kodikos") ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS "ANAPLIRONEI";
CREATE TABLE IF NOT EXISTS "ANAPLIRONEI" (
	"kodikos_prop" integer,
	"kodikos_arxikis_kratisis" integer NOT NULL,
	"kodikos_neas_kratisis" integer default NULL,
	PRIMARY KEY("kodikos_prop","kodikos_arxikis_kratisis","kodikos_neas_kratisis"),
	FOREIGN KEY ("kodikos_neas_kratisis") REFERENCES "KRATISI" ("kodikos") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY ("kodikos_arxikis_kratisis" ) REFERENCES "KRATISI" ("kodikos") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("kodikos_prop") REFERENCES "PROPONITIS"("kodikos") ON DELETE SET NULL ON UPDATE CASCADE
);



DROP TABLE IF EXISTS "MELOS";
CREATE TABLE IF NOT EXISTS "MELOS" (
	"kodikos" integer NOT NULL,
	"onoma" TEXT NOT NULL,
	"eponimo" TEXT NOT NULL,
	"im_eggrafis" TEXT NOT NULL,
	"tilefono"     INTEGER NOT NULL,
	"filo" text NOT NULL,
	"ilikiako_euros" text NOT NULL,
	PRIMARY KEY ("kodikos" AUTOINCREMENT)	
);

DROP TABLE IF EXISTS "SYMMETEXEI";
CREATE TABLE IF NOT EXISTS "SYMMETEXEI" (
	"kodikos_melous" integer NOT NULL,
	"epipedo_didaskalias" TEXT NOT NULL,
	"etos_didaskalias" TEXT NOT NULL,
	"noumero_didaskalias" integer NOT NULL,
	"imerominia_enarksis" TEXT NOT NULL,
	"imerominia_liksis" TEXT DEFAULT NULL,     
	PRIMARY KEY("kodikos_melous","epipedo_didaskalias","etos_didaskalias","noumero_didaskalias","imerominia_enarksis"),
	FOREIGN KEY("kodikos_melous") REFERENCES "MELOS"("kodikos") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY ("epipedo_didaskalias","etos_didaskalias","noumero_didaskalias") REFERENCES "DIDASKALIA"("epipedo","etos","noumero") ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS "KANEI";
CREATE TABLE IF NOT EXISTS "KANEI" (
	"kod_melous" integer NOT NULL,
	"kod_proponiti" integer DEFAULT NULL,
	"kod_kratisis" integer NOT NULL,
	PRIMARY KEY("kod_melous","kod_proponiti","kod_kratisis"),
	FOREIGN KEY("kod_melous") REFERENCES "MELOS"("kodikos") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("kod_proponiti") REFERENCES "PROPONITIS"("kodikos") ON DELETE SET NULL ON UPDATE CASCADE,
	FOREIGN KEY ("kod_kratisis") REFERENCES "KRATISI"("kodikos") ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS "PLIROMI";
CREATE TABLE IF NOT EXISTS "PLIROMI" (
	"kodikos" integer NOT NULL,
	"imerominia" TEXT NOT NULL,
	"poso" REAL NOT NULL,
	PRIMARY KEY("kodikos" AUTOINCREMENT)
);


DROP TABLE IF EXISTS "PLIRONEI";
CREATE TABLE IF NOT EXISTS "PLIRONEI" (
	"kodikos_melous" integer NOT NULL,
	"kodikos_pliromis" integer NOT NULL,
	"kodikos_kratisis" integer NOT NULL,
	PRIMARY KEY("kodikos_melous","kodikos_pliromis","kodikos_kratisis"),
	FOREIGN KEY("kodikos_melous") REFERENCES "MELOS"("kodikos") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("kodikos_pliromis") REFERENCES "PLIROMI"("kodikos") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY ("kodikos_kratisis") REFERENCES "KRATISI"("kodikos") ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS "EKSOFLEI";
CREATE TABLE IF NOT EXISTS "EKSOFLEI" (
	"kodikos_melous" integer NOT NULL,
	"kodikos_pliromis" integer NOT NULL,
	"epipedo_didaskalias" TEXT NOT NULL,
	"etos_didaskalias" TEXT NOT NULL,
	"noumero_didaskalias" integer NOT NULL,
	"pliroteos_minas" TEXT NOT NULL,
	PRIMARY KEY("kodikos_melous","kodikos_pliromis","epipedo_didaskalias","etos_didaskalias","noumero_didaskalias","pliroteos_minas"),
	FOREIGN KEY("kodikos_melous") REFERENCES "MELOS"("kodikos") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("kodikos_pliromis") REFERENCES "PLIROMI"("kodikos") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY ("epipedo_didaskalias","etos_didaskalias","noumero_didaskalias") REFERENCES "DIDASKALIA"("epipedo","etos","noumero") ON DELETE CASCADE ON UPDATE CASCADE
);


-- H Sqlite dimiourgei automata unique indexes sta gnorismata tou proteuontos kleidiou
-- Epomenos emeis dimiourgoume ta euretiria pou den sximatizontai automata
-- Gia parapompi sto documentation tis sqlite bl. https://www.sqlite.org/withoutrowid.html enotita 3


CREATE UNIQUE INDEX IF NOT EXISTS stoixia_melon
ON MELOS(onoma,eponimo,tilefono);

CREATE UNIQUE INDEX IF NOT EXISTS stoixia_prosopikou
ON PROSOPIKO(onoma,eponimo,tilefono);

CREATE INDEX IF NOT EXISTS imerominia_kratiseon
ON KRATISI(imerominia);

CREATE INDEX IF NOT EXISTS ilikiako_euros
ON DIDASKALIA(ilikiako_euros);

