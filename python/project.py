import os
import random
import sqlite3
from random import randint as ran
import time
import datetime
from datetime import date, timedelta
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import unicodedata as ud

import time


class Utility():

    '''Periexi xristikes sinartisis pou xrisimopoiountai apo  tis klasis Simulate kai Gui'''
    
    @staticmethod
    def create_connection():
        try:
            conn=Utility.start_con()
            conn.execute('PRAGMA foreign_keys = ON')
            return conn

        except Exception as e: print(e)

    @staticmethod
    def start_con():
        #os.path.normpath()

        parent_dir= os.path.normpath(os.path.dirname (os.path.dirname(__file__)))   
        db_path = os.path.join(parent_dir,"project","project.db")

        if os.path.isfile(db_path):

            return sqlite3.connect(db_path);
            
        else:
            
            raise Exception("Database not found")

    @staticmethod                
    def read_file(file_path,l): 

        try:
            with open(file_path,'r',encoding='utf-8') as file:
                for line in file:
                    l.append(line.rstrip())
        except OSError as e:
            print("File read failed")

    @staticmethod
    def convert_weekday_to_weekdayInt(weekday):
        
        if (weekday=='ΔΕΥΤΕΡΑ'): return 0
        if (weekday=='ΤΡΙΤΗ'): return 1
        if (weekday=='ΤΕΤΑΡΤΗ'): return 2
        if (weekday=='ΠΕΜΠΤΗ'): return 3
        if (weekday=='ΠΑΡΑΣΚΕΥΗ'): return 4
        if (weekday=='ΣΑΒΒΑΤΟ'): return 5
        if (weekday=='ΚΥΡΙΑΚΗ'): return 6
        
    @staticmethod
    def convert_dateObject_to_weekday(datetime):
        #p.x. datetime='2023-04-23'

        number=datetime.date().weekday()
        if(number==0): result="ΔΕΥΤΕΡΑ"
        if(number==1): result="ΤΡΙΤΗ"
        if(number==2): result="ΤΕΤΑΡΤΗ"
        if(number==3): result="ΠΕΜΠΤΗ"
        if(number==4): result="ΠΑΡΑΣΚΕΥΗ"
        if(number==5): result="ΣΑΒΒΑΤΟ"
        if(number==6): result="ΚΥΡΙΑΚΗ"
        
        return result
    
    @staticmethod
    def convert_date_to_dateObject(date):
        
        datetime_object = datetime.datetime.strptime(date, '%Y-%m-%d')
        
        return datetime_object

    @staticmethod
    def break_strDate_to_integers(date):

        #p.x. date='2023-9-1'  => year=2023 month=9 and day=1

        year,month,day=date.split('-')
        return int(year),int(month),int(day)

    @staticmethod
    def find_all_dates(startDate, endDate,day_of_week):

        # p.x.  date_start = '2023-09-01'   kai    date_end = '2024-08-31'
        # Monday=0 , ... Sunday=6
        # result=['2023-09-03', '2023-09-10',...]

        res_start=Utility.break_strDate_to_integers(startDate)
        year_start=res_start[0]
        month_start=res_start[1]
        day_start=res_start[2]

        res_end=Utility.break_strDate_to_integers(endDate)
        year_end=res_end[0]
        month_end=res_end[1]
        day_end=res_end[2]

        start=date(year_start,month_start,day_start)
        end=date(year_end,month_end,day_end)

        total_days = (end - start).days + 1
        all_days = [start + timedelta(days=day) for day in range(total_days)]
        date_tuples= [day.timetuple()[0:3] for day in all_days if day.weekday() is day_of_week]
        res=[]
        for imerominia in date_tuples:
            res.append(Utility.format_date(imerominia[0],imerominia[1],imerominia[2]))
        return res

    @staticmethod
    def format_date(year,month,day):
        #p.x. year=2019, month=5 , day=8 =>  result='2019-05-08'
        day=str(day)
        if (len(day)==1):
            day='0'+day
        month=str(month)
        if (len(month)==1):
            month='0'+month
        year=str(year)
        return year+'-'+month+'-'+day

    @staticmethod
    def  break_initial_hour_and_minutes(ora):
        #p.x. ora='09:20-10:20'   res=9,20
        arxiki_ora=ora.split('-')
        ora,lepta=(arxiki_ora[0].split(':'))
        return int(ora),int(lepta)

    @staticmethod 
    def find_diathesimi_ora_kai_proponiti(conn,ora,lepta):
        #Theloume enas proponitis na einai diathesimos sinexomena gia ora+lepta xrono

        'Epistrefei ton kodiko,tin ora,ta lepta pou arxizei na einai diathesimos kapoios proponitis kai ti mera. An den iparxei dimiourgi error'    

        kodikoi_proponiton=Sql.find_kodikous_proponiton(conn)
        random.shuffle(kodikoi_proponiton)
        for kodiko in kodikoi_proponiton:
            desmeumenes_ores_didaskalias=Sql.find_desmeumenes_ores_didaskalias_proponiti(conn,kodiko)


            orario=Sql.find_orario_proponiti(conn,kodiko)
            random.shuffle(orario)
            #desmeumenes_ores_didaskalias=Sql.find_desmeumenes_ores_didaskalias_proponiti(conn,kodiko)
            res=Utility.diathesimi_ora(orario,ora,lepta,desmeumenes_ores_didaskalias)
            if(res!=None):
                ora,lepta,mera=res
                return(kodiko,ora,lepta,mera)

        raise Exception("Den brethike eleutheros proponitis")
        
    @staticmethod 
    def diathesimi_ora(meres_kai_ores_pou_mporei_na_doulepsi,sinexomenes_diathesimes_ores,diathesima_lepta,meres_kai_ores_pou_einai_desmeumenes):
        #Epistrefei mia ora kai mera opou einai eleutheros gia tis apaitoumenes sinexomenes ores kai lepta. An den iparxi epistrefi Νone

        # p.x. meres_kai_ores_pou_mporei_na_doulepsi=[('08:20-13:30', 'ΔΕΥΤΕΡΑ')] 
        # p.x. meres_kai_ores_pou_einai_desmeumenes=[ ('09:00-10:00', 'ΔΕΥΤΕΡΑ') , ('10:10-11:10', 'ΔΕΥΤΕΡΑ') ] 
        for kataxorisi in meres_kai_ores_pou_mporei_na_doulepsi:
            orario,mera=kataxorisi

            liksi=orario[6:]
            ora_liksis=int(liksi[0:2])
            lepta_liksis=int(liksi[3:5])
            
            arxi=orario[0:5]
            arxiki_ora=int(arxi[0:2])
            arxika_lepta=int(arxi[3:5])
            
            i_ora=arxiki_ora
            i_lepta=arxika_lepta

            while( (i_ora+sinexomenes_diathesimes_ores)*60 + diathesima_lepta+arxika_lepta <= ora_liksis*60+lepta_liksis):
                # An i_ora=9 kai i_lepta=20 kai sinexomenes_diathesimes_ores=1 simeni oti ergazetai sigoura ali mia ora, mexri tis 10:20
                if(Utility.eleutheros(i_ora,i_lepta,mera,sinexomenes_diathesimes_ores,diathesima_lepta,meres_kai_ores_pou_einai_desmeumenes)):return(i_ora,i_lepta,mera)
                i_ora +=1
        return None

    @staticmethod             
    def eleutheros(ora,lepta,mera,sinexomenes_diathesimes_ores,sinexomena_diathesima_lepta,meres_kai_ores_pou_einai_desmeumenes):

        # Epistrefei true an gia tin zitoumeni arxiki ora kai lepta einai diathesimos gia sinexomenes diathesimes ores kai lepta
        diathesimos=True      

        for kataxorisi in meres_kai_ores_pou_einai_desmeumenes:
            orario_alis_didaskalias,mera_alis_didaskalias= kataxorisi
            if(mera_alis_didaskalias==mera):
                ora_enarksis_alis_didaskalias=int(orario_alis_didaskalias[0:2])
                lepta_enarksis_alis_didaskalias=int(orario_alis_didaskalias[3:5])

                ora_liksis_alis_didaskalias=int(orario_alis_didaskalias[6:8])
                lepta_liksis_alis_didaskalias=int(orario_alis_didaskalias[9:11])

                enarksi_alis_didaskalias= ora_enarksis_alis_didaskalias*60+lepta_enarksis_alis_didaskalias
                liksi_alis_didaskalias= ora_liksis_alis_didaskalias*60+ lepta_liksis_alis_didaskalias

                enarksi_oras= ora*60+lepta
                liksi_oras= (ora+sinexomenes_diathesimes_ores)*60+lepta+sinexomena_diathesima_lepta

                if( enarksi_alis_didaskalias<liksi_oras<=liksi_alis_didaskalias): diathesimos=False
                if( enarksi_alis_didaskalias<=enarksi_oras<liksi_alis_didaskalias): diathesimos=False

        return diathesimos

    @staticmethod
    def dimiourgia_kratiseon_gia_didaskalia(conn,epipedo,etos,noumero,start_date,end_date,epithimitos_kodikos_gipedou):
        res=Sql.find_ores_kai_meres_didaskalias(conn,epipedo,etos,noumero)
        kodikoi_gipedon=Sql.find_kodikous_gipedon(conn)
        if(epithimitos_kodikos_gipedou!=None):
            kodikoi_gipedon=[epithimitos_kodikos_gipedou]+kodikoi_gipedon
       
        
        for kataxorisi in res:
            
            ora_string=kataxorisi[0]
            mera=kataxorisi[1]
            mera_int=Utility.convert_weekday_to_weekdayInt(mera)
            dates=Utility.find_all_dates(start_date,end_date,mera_int)
            ores,lepta=Utility.calculate_ores_kai_lepta(ora_string)
            
            for imerominia in dates:
                found=False
                
                for gipedo in kodikoi_gipedon:

                    #desmeumenes_ores_kai_imerominia=Sql.find_ores_kai_imerominia_pou_einai_desmeumeno_to_gipedo_gia_mia_imerominia(conn,gipedo,imerominia)


                    #res=Utility.eleutheros(arxiki_ora,arxika_lepta,imerominia,ores,lepta,desmeumenes_ores_kai_imerominia)
                    res=Elegxoi.check_if_gipedo_is_available(conn,gipedo,imerominia,ora_string,ores,lepta)

                    if (res):
                        found=True
                        
                        Sql.insert_kratisi(conn,imerominia,ora_string,gipedo)
                        kodikos_kratisis=Sql.find_kodikos_kratisis(conn,imerominia,ora_string,0,gipedo)
                        Sql.insert_dimiourgei(conn,epipedo,etos,noumero,kodikos_kratisis)

                        break
                if(found==False) :print("Gipedo not found for imerominia ",imerominia)


    @staticmethod
    def calculate_ores_kai_lepta(str):
        #p.x. gia str='08:50-13:20'  epistrefei ores=4 kai lepta=30

        lepta_end=int(str[9:11])
        lepta_start=int(str[3:5])
        ora_start=int(str[0:2])
        ora_end=int(str[6:8])

        sinolika_lepta=(ora_end-ora_start)*60+lepta_end-lepta_start

        ores=sinolika_lepta//60
        lepta=sinolika_lepta-ores*60

        return ores,lepta

    @staticmethod   # Gia dimiourgia kainourgiou mathimatos
    def find_kodikous_aneksartiton_kratiseon_proponiti_pou_epikaliptontai_apo_mia_ora_kai_mera_mathimatos(conn,kodikos_proponiti,mera_mathimatos,ora_mathimatos):
        
        melontikes_aneksartites_kratisis_proponiti=Sql.find_melontikes_aneksartites_kratisis_proponiti(conn,kodikos_proponiti) #ora_didaskalias mera_didaskalias
        res=[]
        arxiki_ora_mathimatos,arxika_lepta_mathimatos=Utility.break_initial_hour_and_minutes(ora_mathimatos)

        for kratisi in melontikes_aneksartites_kratisis_proponiti:
            kodikos_kratisis=kratisi[0]
            imerominia_kratisis=kratisi[1]
            ora_kratisis=kratisi[2]
            mera_kratisis=Utility.convert_dateObject_to_weekday(Utility.convert_date_to_dateObject(imerominia_kratisis))
            if(mera_kratisis==mera_mathimatos):
                desmeumenes_meres_kai_ores=(ora_kratisis,mera_kratisis)
                epikalipsi=not Utility.eleutheros(arxiki_ora_mathimatos,arxika_lepta_mathimatos,mera_mathimatos,1,0,desmeumenes_meres_kai_ores)
                if(epikalipsi): res.append(kodikos_kratisis)
        return res

    @staticmethod
    def extract_one_tuple_value(data):
        #Afora periptosis opou ginetai select gia ena mono gnorisma. Epistrefei lista
        #To fetchall() epistrefei lista apo pliades. To extract_one_tuple_value epistrefei lista
        res=[]
        for kataxorisi in data:
            res.append(kataxorisi[0])
            
        return res

    @staticmethod
    def xroniko_diastima_aniki_orario(ora,lepta,mera,sinexomenes_diathesimes_ores,sinexomena_diathesima_lepta,meres_kai_ores_pou_douleui):

        # Epistrefei true an gia tin zitoumeni arxiki ora kai lepta to orario tou periexei sinexomenes diathesimes ores kai lepta
        #p.x. ora=16 lepta=20 sinexomenes_diathesimes_ores=1 sinexomena_diathesima_lepta=30
        diathesimos=False      

        for kataxorisi in meres_kai_ores_pou_douleui:
            orario_doulias,mera_doulias= kataxorisi
            if(mera_doulias==mera):
                ora_enarksis_doulias=int(orario_doulias[0:2])
                lepta_enarksis_doulias=int(orario_doulias[3:5])

                ora_liksis_doulias=int(orario_doulias[6:8])
                lepta_liksis_doulias=int(orario_doulias[9:11])

                enarksi_mathimatos= ora*60+lepta
                liksi_mathimatos= enarksi_mathimatos+sinexomenes_diathesimes_ores*60+ sinexomena_diathesima_lepta

                enarksi_orariou=ora_enarksis_doulias*60+lepta_enarksis_doulias
                liksi_orariou=ora_liksis_doulias*60+lepta_liksis_doulias

                if( enarksi_orariou<= enarksi_mathimatos <= liksi_orariou and enarksi_orariou<= liksi_mathimatos <= liksi_orariou): diathesimos=True

        return diathesimos

    @staticmethod ####change
    def dimiourgia_ksexoristis_kratisis(conn,imerominia,ora,arithmos_gipedou,kodikos_melous,kodikos_proponiti):
        # Dimiourgnountai kratisis eite me proponiti eite xoris
        # Elegxoume oti to gipedo einai eleuthero, o proponitis exei tin ora mesa sto orario tou, o proponitis den exei didaskalia ekeini tin ora kai o proponitis
        # den exei ali kratisi ekeini tin ora oute anaplirosi

        mera=Utility.convert_dateObject_to_weekday(Utility.convert_date_to_dateObject(imerominia))
        today = Utility.find_current_date()
        result=False
        melontikes_aneksartites_kratisis_proponiti=Sql.find_melontikes_aneksartites_kratisis_proponiti(conn,kodikos_proponiti) #ora_didaskalias mera_didaskalias
        melontikes_anaplirosis=Sql.find_melontikes_anaplirosis_proponiti(conn,kodikos_proponiti)

        aneksartites_kratisis=Utility.extract_sec_and_third_values_from_list_of_tuples(melontikes_aneksartites_kratisis_proponiti)

        anaplirosis=Utility.extract_sec_and_third_values_from_list_of_tuples(melontikes_anaplirosis)
        

        if(imerominia<today):print('Ημερομηνία κράτησης μικρότερη από τη σημερινή')
        elif(not Elegxoi.check_if_gipedo_is_available(conn,arithmos_gipedou,imerominia,ora,1,0)): print('Το γήπεδο δεν είναι διαθέσιμο')
        elif(kodikos_proponiti == None or Elegxoi.check_if_proponitis_is_available(conn,kodikos_proponiti,ora,mera,imerominia,aneksartites_kratisis,anaplirosis)[0]):
            Sql.insert_kratisi(conn,imerominia,ora,arithmos_gipedou)
            kodikos_kratisis=Sql.find_kodikos_kratisis(conn,imerominia,ora,0,arithmos_gipedou)
            Sql.insert_into_kanei(conn,kodikos_melous,kodikos_proponiti,kodikos_kratisis)
            
            result=True
        
        return result

    @staticmethod
    def find_current_date():
        return str(datetime.date.today())

    @staticmethod
    def bres_mines_pou_anikoun_se_ena_diastima(start,end):
        # p.x. start=  '2023-10-06'    end='2024-3-25'   res=[Οκτωβριος,Νοεμβριος,Δεκεμβριος,Ιανουαριος,Φεβρουαριος,Μαρτιος]
        
        if end is None: end=Utility.find_current_date()
        mines=['ΙΑΝΟΥΑΡΙΟΣ','ΦΕΒΡΟΥΑΡΙΟΣ','ΜΑΡΤΙΟΣ','ΑΠΡΙΛΙΟΣ','ΜΑΙΟΣ','ΙΟΥΝΙΟΣ','ΙΟΥΛΙΟΣ','ΑΥΓΟΥΣΤΟΣ','ΣΕΠΤΕΜΒΡΙΟΣ','ΟΚΤΩΒΡΙΟΣ','ΝΟΕΜΒΡΙΟΣ','ΔΕΚΕΜΒΡΙΟΣ']
        res=[]

        year_start,month_start,day_start=Utility.break_strDate_to_integers(start)
        year_end,month_end,day_end=Utility.break_strDate_to_integers(end)

        month=month_start

        while(month!=month_end):
            res.append(mines[month-1])
            
            if(month==12):month=1
            else: month +=1

        res.append(mines[month-1])

        return res

    @staticmethod
    def find_diafora_liston(a,b):
        #a-b

        d=[x for x in a if x not in b]
        return d

    @staticmethod
    def antistoixise_mina_se_noumero(minas):
        if (minas=='ΙΑΝΟΥΑΡΙΟΣ'): return 1
        if (minas=='ΦΕΒΡΟΥΑΡΙΟΣ'): return 2
        if (minas=='ΜΑΡΤΙΟΣ'): return 3
        if (minas=='ΑΠΡΙΛΙΟΣ'): return 4
        if (minas=='ΜΑΙΟΣ'): return 5
        if (minas=='ΙΟΥΝΙΟΣ'): return 6
        if (minas=='ΙΟΥΛΙΟΣ'): return 7
        if (minas=='ΑΥΓΟΥΣΤΟΣ'): return 8
        if (minas=='ΣΕΠΤΕΜΒΡΙΟΣ'): return 9
        if (minas=='ΟΚΤΩΒΡΙΟΣ'): return 10
        if (minas=='ΝΟΕΜΒΡΙΟΣ'): return 11
        if (minas=='ΔΕΚΕΜΒΡΙΟΣ'): return 12

    @staticmethod
    def find_aplirotous_mines_gia_mia_didaskalia_gia_ena_atomo(conn,kodiko,epipedo,etos,noumero,imerominia_enarksis,imerominia_liksis):
        mines_pou_simetexei_se_didaskalia=Utility.bres_mines_pou_anikoun_se_ena_diastima(imerominia_enarksis,imerominia_liksis)
        mines_pou_exei_plirosi=Sql.find_pliromenous_mines_gia_didaskalia(conn,kodiko,epipedo,etos,noumero)
        mines_pou_prepei_na_plirosi=Utility.find_diafora_liston(mines_pou_simetexei_se_didaskalia,mines_pou_exei_plirosi)
        return mines_pou_prepei_na_plirosi

    @staticmethod
    def find_aplirotes_kai_pliromenes_didaskalies_atomou(conn,kodikos,etos):
        didaskalies_melous=Sql.find_didaskalies_pou_simmetexei_ena_atomo_gia_ena_xrono(conn,kodikos,etos)
        aplirotes_diaskalies=[]
        pliromenes_didaskalies=[]
        for didaskalia in didaskalies_melous:
            kod,epipedo,etos,noumero,imerominia_enarksis,imerominia_liksis=didaskalia
            poso=Sql.find_kostos_didaskalias(conn,epipedo,etos,noumero)

            aplirotoi_mines=Utility.find_aplirotous_mines_gia_mia_didaskalia_gia_ena_atomo(conn,kodikos,epipedo,etos,noumero,imerominia_enarksis,imerominia_liksis)
            mines_pou_exei_plirosi=Sql.find_pliromenous_mines_gia_didaskalia(conn,kodikos,epipedo,etos,noumero)
            for mina in aplirotoi_mines:
                aplirotes_diaskalies.append((epipedo,etos,noumero,mina,poso))
            for mina in mines_pou_exei_plirosi:
                pliromenes_didaskalies.append((epipedo,etos,noumero,mina,poso))
        return aplirotes_diaskalies,pliromenes_didaskalies

    @staticmethod
    def find_oles_tis_aplirotes_didaskalies(conn,etos):
        kodikoi_atomon=Sql.find_kodikous_melon(conn)
        res=[]
        for melos in kodikoi_atomon:
            aplirotes_didaskalies_atomou=Utility.find_aplirotes_kai_pliromenes_didaskalies_atomou(conn,melos,etos)[0]
            if(len(aplirotes_didaskalies_atomou)!=0):
                aplirotes_didaskalies_atomou=list(aplirotes_didaskalies_atomou)
                aplirotes_didaskalies_atomou.insert(0,melos)
                aplirotes_didaskalies_atomou=tuple(aplirotes_didaskalies_atomou)
                res.append(aplirotes_didaskalies_atomou)
        return res

    @staticmethod
    def extract_sec_and_third_values_from_list_of_tuples(list):
        res=[]

        for kataxorisi in list:
            res.append((kataxorisi[1],kataxorisi[2]))
        return res

    @staticmethod
    def find_date_of_next_year():
        # An today='2023-12-11' Epistrefei '2024-12-11'

        today=Utility.find_current_date()

        next_year=str(int(today[0:4])+1)+today[4:]

        return next_year

    @staticmethod
    def find_current_year_period():
        # Epistrefei to fetino etos didaskalion . P.x. 2023-2024
        a=Utility.find_current_date()   
        month=int(a[5:7])
        if(month>=9): # Ton septembrio allazei etos didaskalias
            b=Utility.find_date_of_next_year()
            c=a[0:4]+"-"+b[0:4]
        
        elif(month<8):
            etos_pou_telioni_i_didaskalia=int(a[0:4])
            etos_pou_ksekinise_i_didaskalia=etos_pou_telioni_i_didaskalia-1
            c=str(etos_pou_ksekinise_i_didaskalia)+'-'+str(etos_pou_telioni_i_didaskalia)

        return c

    @staticmethod
    def pliromi_kratisis(conn,imerominia_pliromis,kratisi,kodiko_melous):
        poso=Sql.find_kostos_aneksartitis_kratisis(conn,kratisi)
        Sql.insert_pliromi(conn,imerominia_pliromis,poso)
        kodikos_pliromis=Sql.find_kodikos_proigoumenis_isaxthisas_timis_pinaka(conn,'PLIROMI')
        Sql.insert_plironei(conn,kodiko_melous,kodikos_pliromis,kratisi)

    @staticmethod
    def pliromi_didaskalias(conn,imerominia_pliromis,kodiko_melous,epipedo,etos,noumero,mina):
        poso=Sql.find_kostos_didaskalias(conn,epipedo,etos,noumero)
        Sql.insert_pliromi(conn,imerominia_pliromis,poso)
        kodikos_pliromis=Sql.find_kodikos_proigoumenis_isaxthisas_timis_pinaka(conn,'PLIROMI')
        Sql.insert_eksoflei(conn,kodiko_melous,kodikos_pliromis,epipedo,etos,noumero,mina)

    @staticmethod
    def convert_ora(ora_int,lepta_int):
        # p.x. an ora_int=9 kai lepta_int=5 epistrefei 09:05-10:05
        # Ta mathimata einai mia ora

        ora=str(ora_int)
        if (len(ora)==1):
            ora='0'+ora
        lepta= str(lepta_int)
        if(len(lepta)==1):lepta='0'+lepta
        teliki_ora=str(ora_int+1)
        if (len(teliki_ora)==1):
            teliki_ora='0'+teliki_ora
        ora=ora+':'+lepta+'-'+teliki_ora+':'+lepta
        return ora

class atomoCreator():

    '''Dimiourgei profil atomon'''

    'An pinakas=melos gemizei ta meli kai an pinakas=prosopiko to prosopiko'


    def __init__(self):
        self.andrika_onomata=[]
        self.andrika_eponima=[]
        self.ginaikia_onomata=[]
        self.ginaikia_eponima=[]
        self.read_names()


    def read_names(self):
        
        path_python= os.path.dirname(__file__)

        path_andrika_onomata=  os.path.join(path_python,"arxia_gia_prosomiosi","andrika_onomata.txt")
        path_andrika_eponima=  os.path.join(path_python,"arxia_gia_prosomiosi","andrika_eponima.txt")
        path_ginaikia_onomata=  os.path.join(path_python,"arxia_gia_prosomiosi","ginaikia_onomata.txt")
        path_ginaikia_eponima=  os.path.join(path_python,"arxia_gia_prosomiosi","ginaikia_eponima.txt")

        Utility.read_file(path_andrika_onomata,self.andrika_onomata)
        Utility.read_file(path_andrika_eponima,self.andrika_eponima)
        Utility.read_file(path_ginaikia_onomata,self.ginaikia_onomata)
        Utility.read_file(path_ginaikia_eponima,self.ginaikia_eponima)

    def create_onomateponimo(self):

        # O gia antra, 1 gia ginaika
        genos=ran(0,1)
        

        if (genos==0):

            onoma= self.andrika_onomata[ran (0, len(self.andrika_onomata)-1)]
            eponimo= self.andrika_eponima[ran (0, len(self.andrika_eponima)-1)]
            filo='Α'

        else:
            onoma=self.ginaikia_onomata[ran (0, len(self.ginaikia_onomata)-1)]
            eponimo= self.ginaikia_eponima[ran (0, len(self.ginaikia_eponima)-1)]
            filo='Θ'

        return onoma,eponimo,filo

    def create_imeromia_eggrafis(self):

        year=str(ran(1990,2023))
        month=str(ran(1,12))

        if month in('4','6','9'): date=str(ran(1,30))
        elif month in('2') :  date=str(ran(1,28))
        else:               date=str(ran(1,31))
        
        if(len(month)==1): month= '0'+month
        if(len(date)==1):  date= '0'+date

        return year+'-'+month+'-'+date

    def create_tilefono(self):

        tilefono=ran(6900000000,6999999999)

        return tilefono

    def fill_atomo(self,i,pinakas):

        'An pinakas=melos gemizei ta meli kai an pinakas=prosopiko to prosopiko'

        
        conn=Utility.create_connection()
        if(pinakas=='melos'):
            while(i>0):
                onoma,eponimo,filo= self.create_onomateponimo()
                imerominia_eggrafis=self.create_imeromia_eggrafis()
                tilefono=self.create_tilefono()
                ilikiako_euros=Simulate.create_ilikiako_euros()
                

                if(not Elegxoi.melosExists(onoma,eponimo,tilefono)):
                        Sql.add_melos(conn,onoma,eponimo,imerominia_eggrafis,tilefono,filo,ilikiako_euros)
                        i = i-1
        elif(pinakas=='prosopiko'):
            while(i>0):
                onoma,eponimo,filo= self.create_onomateponimo()
                tilefono=self.create_tilefono()
                

                if(not Elegxoi.prosopikoExists(onoma,eponimo,tilefono)):
                        Sql.add_prosopiko(conn,onoma,eponimo,tilefono,filo)
                        i = i-1

        conn.close()

class Elegxoi():
    '''Υλοποιεί  ελέγχους για την εγκυρότητα των δεδομένων'''

    @staticmethod
    def melosExists(onoma,eponimo,tilefono):

        conn=Utility.create_connection()
        cursor=conn.cursor()

        cursor.execute('''  Select *
                            from melos
                            where onoma=? and eponimo=? and tilefono=?''',[onoma,eponimo,tilefono])
        data=cursor.fetchall()
        cursor.close()
        conn.close()

        if(len(data)==0):return False
        else: return True

    @staticmethod
    def prosopikoExists(onoma,eponimo,tilefono):

        conn=Utility.create_connection()
        cursor=conn.cursor()

        cursor.execute('''  Select *
                            from prosopiko
                            where onoma=? and eponimo=? and tilefono=?''',[onoma,eponimo,tilefono])
        data=cursor.fetchall()
        cursor.close()
        conn.close()


        if(len(data)==0):return False
        else: return True

    @staticmethod
    def check_if_didaskalia_is_full(conn,epipedo_didaskalias,etos_didaskalias,noumero_didaskalias):
        meli=Sql.find_energa_meli_mias_didaskalias(conn,epipedo_didaskalias,etos_didaskalias,noumero_didaskalias)
        if (len(meli)==4): return True
        else: return False

    @staticmethod
    def check_melos_idi_simetexei_se_didaskalia(conn,kodikos_melous,epipedo_didaskalias,etos_didaskalias,noumero_didaskalias):
        count=Sql.count_tautoxrones_simetoxes_melous_se_idia_didaskalia(conn,kodikos_melous,epipedo_didaskalias,etos_didaskalias,noumero_didaskalias)
        if(count==0): return False
        else: return True
    
    @staticmethod
    def check_if_proponitis_einai_desmeumenos_logo_didaskalias_mia_ora_kai_mera(conn,kodikos,ora,mera):
        desmeumenes_ores_kai_meres=Sql.find_desmeumenes_ores_didaskalias_proponiti(conn,kodikos)
        arxiki_ora,arxika_lepta=Utility.break_initial_hour_and_minutes(ora)
        return not Utility.eleutheros(arxiki_ora,arxika_lepta,mera,1,0,desmeumenes_ores_kai_meres)
    
    @staticmethod
    def check_if_gipedo_is_available(conn,gipedo,imerominia,ora,diathesimes_ores,diathesima_lepta):
        arxiki_ora,arxika_lepta=Utility.break_initial_hour_and_minutes(ora)
        desmeumenes_ores_kai_imerominia=Sql.find_ores_kai_imerominia_pou_einai_desmeumeno_to_gipedo_gia_mia_imerominia(conn,gipedo,imerominia)
        res=Utility.eleutheros(arxiki_ora,arxika_lepta,imerominia,diathesimes_ores,diathesima_lepta,desmeumenes_ores_kai_imerominia)
        return res

    @staticmethod
    def check_if_proponitis_exei_epikalipsi_gia_sigkekrimeni_ora_kai_imerominia(conn,kodikos_proponiti,imerominia,ora,kratisis):
        #Oi kratisis einai tis morfis [(imerominia,ora)...]


        arxiki_ora_mathimatos,arxika_lepta_mathimatos=Utility.break_initial_hour_and_minutes(ora)
        for kratisi in kratisis:

            imerominia_kratisis=kratisi[0]
            ora_kratisis=kratisi[1]
            if(imerominia_kratisis==imerominia):
                epikalipsi= not Utility.eleutheros(arxiki_ora_mathimatos,arxika_lepta_mathimatos,imerominia,1,0,[(ora_kratisis,imerominia_kratisis)])
                if(epikalipsi):return True
        return False

    @staticmethod
    def check_ora_in_orario_proponiti(conn,kodikos,ora,mera):
        
        programa=Sql.find_orario_proponiti(conn,kodikos)
        arxiki_ora,arxika_lepta=Utility.break_initial_hour_and_minutes(ora)
        ergazetai= Utility.xroniko_diastima_aniki_orario(arxiki_ora,arxika_lepta,mera,1,0,programa) 
        return ergazetai   

    @staticmethod
    def check_if_proponitis_is_available(conn,kodikos_proponiti,ora,mera,imerominia,aneksartites_kratisis,anaplirosis):
        
        res=(True,-1)
        if( not Elegxoi.check_ora_in_orario_proponiti(conn,kodikos_proponiti,ora,mera)):
            print('Η ωρα δεν ανηκει στο ωραριο του προπονητη')
            res=(False,0)
        if( Elegxoi.check_if_proponitis_einai_desmeumenos_logo_didaskalias_mia_ora_kai_mera(conn,kodikos_proponiti,ora,mera)):
            print('Ο προπονητής έχει εκείνη την ώρα διδασκαλία')
            res=(False,1)
        if( Elegxoi.check_if_proponitis_exei_epikalipsi_gia_sigkekrimeni_ora_kai_imerominia(conn,kodikos_proponiti,imerominia,ora,aneksartites_kratisis)):
            print(('Ο προπονητής έχει εκείνη την ώρα άλλη κράτηση'))
            res=(False,2)
        if( Elegxoi.check_if_proponitis_exei_epikalipsi_gia_sigkekrimeni_ora_kai_imerominia(conn,kodikos_proponiti,imerominia,ora,anaplirosis)):
            print(('Ο προπονητής έχει εκείνη την ώρα αναπληρωση'))
            res=(False,3)
        return res

    @staticmethod
    def check_sinonimia(conn,onoma,eponimo):
        tilefona=Sql.find_tilefono_prosopikou(conn,onoma,eponimo)
        if(len(tilefona)>1):
            return True
        else: return False

class Sql():
    '''Περιέχει τις SQL εντολές'''

    @staticmethod
    def add_melos(conn,onoma,eponimo,imerominia_eggrafis,tilefono,filo,ilikiako_euros):
        conn.execute(''' insert into MELOS(onoma,eponimo,im_eggrafis,tilefono,filo,ilikiako_euros)
                         values(?,?,?,?,?,?)''',[onoma,eponimo,imerominia_eggrafis,tilefono,filo,ilikiako_euros] )
        conn.commit()

    @staticmethod
    def add_prosopiko(conn,onoma,eponimo,tilefono,filo):
        conn.execute(''' insert into PROSOPIKO (onoma,eponimo,tilefono,imerominia_proslipsis,filo)
                         values(?,?,?,date(),? )''',[onoma,eponimo,tilefono,filo] )
        conn.commit()

    @staticmethod
    def find_kodikous_of_all_prosopiko(conn):
        cursor=conn.cursor()
        cursor.execute('''Select kodikos from prosopiko''')
        kodikoi=[]
        data=cursor.fetchall()
        for i in data:
            kodikoi.append(i[0])
        return kodikoi

    @staticmethod
    def insert_grammatea(conn,kodikos,misthos):
        conn.execute('''insert into GRAMMATEAS values(?,?)''',[kodikos,misthos])
        conn.commit()

    @staticmethod
    def insert_sintiriti(conn,kodikos,misthos):
        conn.execute('''insert into SINTIRITIS values(?,?)''',[kodikos,misthos])
        conn.commit()

    @staticmethod
    def insert_proponiti(conn,kodikos):
        conn.execute('''insert into PROPONITIS(kodikos) values(?)''',[kodikos])
        conn.commit()

    @staticmethod
    def empty_table(conn,pinakas):
        conn.execute('''delete from {}'''.format(pinakas))
        conn.commit()

    @staticmethod
    def insert_mathima(conn,epipedo,ores):
        conn.execute('''insert into mathima values(?,?)''',[epipedo,ores])
        conn.commit()

    @staticmethod
    def insert_gipedo(conn,idos,dieuthinsi):
        conn.execute('''insert into gipedo(eidos_gipedou,dieuthinsi)
                        values(?,?)''',[idos,dieuthinsi])
        conn.commit()

    @staticmethod
    def insert_didaskalia(conn,epipedo,etos,noumero,kostos,ilikiako_euros):
        conn.execute('''insert into didaskalia 
                        values(?,?,?,?,?)''',[epipedo,etos,noumero,kostos,ilikiako_euros])
        conn.commit()
    
    @staticmethod
    def find_dinata_epipeda(conn):
        cursor=conn.cursor()
        cursor.execute('''Select  epipedo,ores_ana_ebdomada from mathima''')
        epipeda_ores=cursor.fetchall()
        dinata_epipeda=[]   
        ores=[]
        for kataxorisi in epipeda_ores:
            dinata_epipeda.append(kataxorisi[0])
            ores.append(kataxorisi[1])
        return (dinata_epipeda,ores)

    @staticmethod
    def find_kodikos_melous(conn,onoma,eponimo,tilefono):
        cursor=conn.cursor()
        cursor.execute('''select kodikos from melos where onoma=? and eponimo=? and tilefono=?''',[onoma,eponimo,tilefono])
        data=cursor.fetchall()
        return Utility.extract_one_tuple_value(data)[0]

    @staticmethod
    def find_megalitero_noumero_epipedou(conn,etos,epipedo):
        cursor=conn.cursor()
        cursor.execute('''select max(noumero) from didaskalia where etos=? and epipedo=?''',[etos,epipedo] )
        noumero=cursor.fetchone()
        if noumero==None: return None
        return noumero[0]

    @staticmethod
    def insert_orario(conn,kodikos,ora,mera):
        conn.execute('''insert into PROPONITIS_ORARIO
                        values(?,?,?)''',[kodikos,ora,mera])
        conn.commit()

    @staticmethod
    def find_kodikous_proponiton(conn):
        cursor=conn.cursor()
        cursor.execute('''Select kodikos from proponitis''')
        data=cursor.fetchall()
        kodikoi=[]
        for i in data:
            kodikoi.append(i[0])
        return kodikoi

    @staticmethod
    def find_didaskalies(conn,etos):
        cursor=conn.cursor()
        cursor.execute('''Select * from didaskalia where etos=?''',[etos])
        data=cursor.fetchall()
        return data
    
    @staticmethod
    def find_orario_proponiti(conn,kodikos):
        cursor=conn.cursor()
        cursor.execute('''Select ora,mera from proponitis_orario where kodikos_prop=?''',[kodikos])
        data=cursor.fetchall()
        return data

    @staticmethod
    def find_desmeumenes_ores_didaskalias_proponiti(conn,kodikos):
        # Einai oi ores pou einai desmeumenos gia na kanei kapoia fetini didaskalia

        etos=Utility.find_current_year_period()

        cursor=conn.cursor()
        cursor.execute('''Select ora,mera from pragmatopoiei where kodikos_prop=? and etos_did=?''',[kodikos,etos])
        data=cursor.fetchall()
        return data

    @staticmethod
    def find_didaskalies_proponiti(conn,kodikos,etos):

        cursor=conn.cursor()
        cursor.execute('''Select ora,mera,epipedo_did,etos_did,noumero_did from pragmatopoiei where kodikos_prop=? and etos_did=?''',[kodikos,etos])
        data=cursor.fetchall()
        return data

    @staticmethod
    def insert_pragmatopoiei(conn,kodikos_prop,epip_did,etos,noumero,ora,mera):
        conn.execute('''insert into pragmatopoiei 
                        values (?,?,?,?,?,?)''',[kodikos_prop,epip_did,etos,noumero,ora,mera])
        conn.commit()
  
    @staticmethod
    def find_ebdomadiaies_ores_mathimatos(conn,epipedo):
        cursor=conn.cursor()
        cursor.execute('''select ores_ana_ebdomada from mathima  where epipedo=?''',[epipedo])
        data=cursor.fetchall()
        return data[0][0]

    @staticmethod
    def find_ores_kai_meres_didaskalias(conn,epipedo,etos,noumero):
        cursor=conn.cursor()
        cursor.execute('''select ora,mera from pragmatopoiei where epipedo_did=? and etos_did=? and noumero_did=?''',[epipedo,etos,noumero])
        data=cursor.fetchall()
        return data

    @staticmethod
    def checkIfMathimaAlreadyExistsForADay(conn,epipedo,etos,noumero,mera):
        # elegxei an idi ginetai mathima mia mera gia na min bali deuteri fora didaskalia tin idia mera

        cursor=conn.cursor()
        cursor.execute('''select mera from PRAGMATOPOIEI join  DIDASKALIA on epipedo=epipedo_did and etos=etos_did and noumero=noumero_did
                         where epipedo=? and etos=? and noumero=?''',[epipedo,etos,noumero])
        data=cursor.fetchall()
        result=[]
        for kataxorisi in data:
            result.append(kataxorisi[0])
        return mera in result

    @staticmethod 
    def find_ores_kai_imerominia_pou_einai_desmeumeno_to_gipedo_gia_mia_imerominia(conn,arithmos_gipedou,date):
        # Epistrefei tis ores  pou exoun gini kratisis  gia to gipedo gia tin imerominia
        # p.x. date='2023-09-01'

        cursor=conn.cursor()
        cursor.execute(''' select ora,imerominia
                            from kratisi
                            where arithmos_gipedou=? and imerominia=? and anablithike=false''',[arithmos_gipedou,date])
        data=cursor.fetchall()

        return data
    
    @staticmethod
    def find_kodikous_gipedon(conn):
        cursor=conn.cursor()
        cursor.execute(''' select arithmos_gipedou from gipedo''')
        data=cursor.fetchall()
        res=[]
        for kodiko in data:
            res.append(kodiko[0])
        return res

    @staticmethod
    def insert_kratisi(conn,imerominia,ora,arithmos_gipedou):
        
        conn.execute('''insert into kratisi(imerominia,ora,arithmos_gipedou)
                            values(?,?,?)''',[imerominia,ora,arithmos_gipedou])
        conn.commit()

    @staticmethod
    def find_kodikos_kratisis(conn,imerominia,ora,anablithike,arithmos_gipedou):
        cursor=conn.cursor()
        cursor.execute('''Select kodikos from kratisi
                            where imerominia=? and ora=? and anablithike=? and arithmos_gipedou=?''',[imerominia,ora,anablithike,arithmos_gipedou])
        data=cursor.fetchall()[0][0]
        return data

    @staticmethod
    def insert_dimiourgei(conn,epipedo,etos,noumero,kodikos_kr):
        conn.execute('''insert into dimiourgei values(?,?,?,?)''',[epipedo,etos,noumero,kodikos_kr])
        conn.commit()

    @staticmethod
    def find_kodikous_sintiriton(conn):
        cursor=conn.cursor()
        cursor.execute('Select kodikos from sintiritis')
        data=cursor.fetchall()
        res=[]
        for kataxorisi in data:
            res.append(kataxorisi[0])
        return res

    @staticmethod
    def update_sintiriti_gipedou(conn,kodikos_sintiriti,arithmos_gipedou):
        conn.execute('update GIPEDO set kodikos_sintiriti=?  where arithmos_gipedou=?',[kodikos_sintiriti,arithmos_gipedou])
        conn.commit()

    @staticmethod
    def find_energa_meli_mias_didaskalias(conn,epipedo_didaskalias,etos_didaskalias,noumero_didaskalias):
        cursor=conn.cursor()
        cursor.execute('''select kodikos_melous from SYMMETEXEI
                        where epipedo_didaskalias=? and etos_didaskalias=? and noumero_didaskalias=? and imerominia_liksis is  null''',[epipedo_didaskalias,etos_didaskalias,noumero_didaskalias])
        data=cursor.fetchall()
        res=[]
        for kataxorisi in data:
            res.append(kataxorisi[0])
        return res

    @staticmethod
    def find_kodikous_melon_kai_ilikiako_euros(conn):
        cursor=conn.cursor()
        cursor.execute('''select kodikos,ilikiako_euros from melos''')
        data=cursor.fetchall()
        
        return data

    @staticmethod
    def insert_symetexei(conn,kodikos_melous,epipedo_didaskalias,etos_didaskalias,noumero_didaskalias,imerominia_enarksis):

        conn.execute('''insert INTO SYMMETEXEI(kodikos_melous,epipedo_didaskalias,etos_didaskalias,noumero_didaskalias,imerominia_enarksis)
                        values(?,?,?,?,?)''',[kodikos_melous,epipedo_didaskalias,etos_didaskalias,noumero_didaskalias,imerominia_enarksis])
        conn.commit() 

    @staticmethod
    def appegrafi_from_symetexei(conn,kodikos_melous,epipedo_didaskalias,etos_didaskalias,noumero_didaskalias,imerominia_enarksis,imerominia_liksis):

        conn.execute('''update SYMMETEXEI set imerominia_liksis=?
        where kodikos_melous=? and epipedo_didaskalias=? and etos_didaskalias=? and noumero_didaskalias=? and imerominia_enarksis=?''',[imerominia_liksis,kodikos_melous,epipedo_didaskalias,etos_didaskalias,noumero_didaskalias,imerominia_enarksis])
        conn.commit() 

    @staticmethod
    def count_tautoxrones_simetoxes_melous_se_idia_didaskalia(conn,kodikos_melous,epipedo_didaskalias,etos_didaskalias,noumero_didaskalias):
        cursor=conn.cursor()
        cursor.execute('''select count(*) from SYMMETEXEI
        where kodikos_melous=? and epipedo_didaskalias=? and etos_didaskalias=? and noumero_didaskalias=? and imerominia_liksis is null''',[kodikos_melous,epipedo_didaskalias,etos_didaskalias,noumero_didaskalias])
        return cursor.fetchone()[0]

    @staticmethod
    def find_melontikes_aneksartites_kratisis_proponiti(conn,kod_proponiti):
        cursor=conn.cursor()
        cursor.execute('''select kodikos,imerominia,ora,arithmos_gipedou,dieuthinsi from (kanei join kratisi on kod_kratisis=kodikos) natural join gipedo where imerominia>=date() and kod_proponiti=? and anablithike=0''',[kod_proponiti])
        data=cursor.fetchall()
        return data

    @staticmethod
    def insert_into_kanei(conn,kodikos_melous,kodikos_proponiti,kodikos_kratisis):
        conn.execute('''insert into KANEI values(?,?,?)''',[kodikos_melous,kodikos_proponiti,kodikos_kratisis])
        conn.commit()
        
    @staticmethod
    def find_didaskalies_pou_simmetexei_ena_atomo_gia_ena_xrono(conn,kodikos_melous,etos):
        cursor=conn.cursor()
        cursor.execute('''select * from SYMMETEXEI where kodikos_melous=?  and etos_didaskalias=?
                            order by kodikos_melous,imerominia_enarksis desc''',[kodikos_melous,etos])
        data=cursor.fetchall()
        return data

    @staticmethod
    def find_pliromenous_mines_gia_didaskalia(conn,kodikos,epipedo,etos,noumero):
        cursor=conn.cursor()
        cursor.execute(''' select pliroteos_minas from eksoflei where kodikos_melous=? and epipedo_didaskalias=? and etos_didaskalias=? and noumero_didaskalias=?''',[kodikos,epipedo,etos,noumero])
        data=cursor.fetchall()
        res=Utility.extract_one_tuple_value(data)
        return res

    @staticmethod
    def find_kostos_didaskalias(conn,epipedo,etos,noumero):
        cursor=conn.cursor()
        cursor.execute(''' select miniaio_kostos from didaskalia where epipedo=? and etos=? and noumero=?''',[epipedo,etos,noumero])
        data=cursor.fetchmany()
        res=Utility.extract_one_tuple_value(data)[0]
        
        return res

    @staticmethod
    def find_kodikous_melon(conn):
        cursor=conn.cursor()
        cursor.execute('''select kodikos from melos''')
        data=cursor.fetchall()
        res=Utility.extract_one_tuple_value(data)
        return Utility.extract_one_tuple_value(data)

    @staticmethod
    def insert_pliromi(conn,imerominia,poso):
        conn.execute('''insert into pliromi(imerominia,poso) values(?,?)''',[imerominia,poso])
        conn.commit()

    @staticmethod
    def find_kodikos_proigoumenis_isaxthisas_timis_pinaka(conn,tablename):
        cursor=conn.cursor()
        cursor.execute('''select seq from sqlite_sequence where name=?''',[tablename])
        data=cursor.fetchall()
        return Utility.extract_one_tuple_value(data)[0]

    @staticmethod
    def insert_eksoflei(conn,kodikos_melous,kodikos_pliromis,epipedo_didaskalias,etos_didaskalias,noumero_didaskalias,pliroteos_minas):
        conn.execute('''insert into eksoflei values(?,?,?,?,?,?)''',[kodikos_melous,kodikos_pliromis,epipedo_didaskalias,etos_didaskalias,noumero_didaskalias,pliroteos_minas])
        conn.commit() 

    @staticmethod
    def find_aplirotes_kratisis_atomou_gia_mia_imerominia_kai_prin(conn,kodikos,date):
        #epistrefei tous kodikous ton kratiseon gia idiaitera mathimata pou den exei plirosei
        cursor=conn.cursor()
        cursor.execute('''  select kodikos
                            from (kratisi join KANEI on kodikos=kod_kratisis) left outer join plironei on kodikos= kodikos_kratisis
                            where kod_melous=? and kodikos_pliromis is NULL and imerominia<?''',[kodikos,date])
        data=cursor.fetchall()
        return Utility.extract_one_tuple_value(data)
    
    @staticmethod
    def find_pliromenes_kratisis_atomou(conn,kodikos):
        #epistrefei tous kodikous ton kratiseon gia idiaitera mathimata pou  exei plirosei
        cursor=conn.cursor()
        cursor.execute('''  select kodikos
                            from (kratisi join KANEI on kodikos=kod_kratisis) left outer join plironei on kodikos= kodikos_kratisis
                            where kod_melous=? and kodikos_pliromis is not NULL''',[kodikos])
        data=cursor.fetchall()
        return Utility.extract_one_tuple_value(data)

    @staticmethod
    def insert_plironei(conn,kodikos_melous,kodikos_pliromis,kodikos_kratisis):
        conn.execute('''insert into plironei values(?,?,?)''',[kodikos_melous,kodikos_pliromis,kodikos_kratisis])
        conn.commit()

    @staticmethod
    def find_kostos_aneksartitis_kratisis(conn,kodikos_kratisis):
        cursor=conn.cursor()
        cursor.execute('''  select kostos_mathimatos
                            from PROPONITIS join kanei on kodikos=kod_proponiti
                            where kod_kratisis=?
                            UNION
                            select kostos_aneks_kratisis
                            from kanei join kratisi on kod_kratisis=kodikos natural join gipedo arithmos_gipedou
                            where kod_proponiti is Null and kodikos=? limit 1	''',[kodikos_kratisis,kodikos_kratisis] )

        data=cursor.fetchall()
        return Utility.extract_one_tuple_value(data)[0]

    @staticmethod
    def find_kodikous_ksexoriston_kratiseon(conn):
        cursor=conn.cursor()
        cursor.execute('''Select kod_kratisis from kanei''')
        data=cursor.fetchall()
        return Utility.extract_one_tuple_value(data)

    @staticmethod
    def find_imerominia_dieuthinsi_gipedou_kai_arithmo_gipedou_gia_kratisi(conn,kodikos_kratisis):
        cursor=conn.cursor()
        cursor.execute('''select imerominia,dieuthinsi,arithmos_gipedou,ora from kratisi natural join gipedo where kodikos=?''',[kodikos_kratisis])
        data=cursor.fetchall()[0]
        
        return data[0],data[1],data[2],data[3]

    @staticmethod
    def find_melontikes_anaplirosis_proponiti(conn,kodikos):
        cursor=conn.cursor()
        cursor.execute('''  select kodikos,imerominia,ora,arithmos_gipedou,dieuthinsi
                            from KRATISI join ANAPLIRONEI on kodikos_neas_kratisis=kodikos natural join gipedo
                            where kodikos_prop=? and imerominia>=date() ''',[kodikos])
        data=cursor.fetchall()
        return data

    @staticmethod
    def find_melontikous_kodikous_kratiseon_pou_antistoixoun_se_didaskalies(conn):
        cursor=conn.cursor()
        cursor.execute('''  select kodikos
                            from kratisi join dimiourgei on kodikos_krat=kodikos
                            where imerominia>date() and anablithike=false''')
        data=cursor.fetchall()
        return Utility.extract_one_tuple_value(data)

    @staticmethod
    def anaboli_sigkekrimenis_kratisis(conn,kodikos):
        conn.execute('''update kratisi set anablithike=true where kodikos=?''',[kodikos])
        conn.commit()

    @staticmethod
    def find_kratisi(conn,kodikos):
        cursor=conn.cursor()
        cursor.execute('''select * from kratisi where kodikos=?''',[kodikos])
        data=cursor.fetchall()
        return data[0]

    @staticmethod
    def insert_anaplironei(conn,kod_prop,kod_arxikis_krat,kod_neas_krat):
        conn.execute('''insert into anaplironei values(?,?,?)''',[kod_prop,kod_arxikis_krat,kod_neas_krat])
        conn.commit()

    @staticmethod
    def find_onomateponimo_proponiti_pou_ekane_idiaitero(conn,kodikos_kratisis):
        cursor=conn.cursor()
        cursor.execute('''select onoma,eponimo from prosopiko join kanei on kodikos=kod_proponiti where kod_kratisis=?''',[kodikos_kratisis])
        data=cursor.fetchall()
        if(len(data)==0):return None,None
        return data[0][0],data[0][1]

    @staticmethod
    def find_mi_gemata_group_gia_ilikiako_euros(conn,etos,ilikiako_euros):
        cursor=conn.cursor()
        cursor.execute('''  SELECT epipedo,etos,noumero,miniaio_kostos,ilikiako_euros,count(*) as simetexontes
                            from SYMMETEXEI join DIDASKALIA on epipedo=epipedo_didaskalias and etos=etos_didaskalias and noumero=noumero_didaskalias
                            where imerominia_liksis is null and etos=? and ilikiako_euros=?
                            group by epipedo,etos,noumero,miniaio_kostos,ilikiako_euros
                            having count(*) <4''',[etos,ilikiako_euros])
        data=cursor.fetchall()
        return data

    @staticmethod
    def find_ora_mera_kai_onomateponimo_proponiti_gia_didaskalia(conn,epipedo,etos,noumero):
        cursor=conn.cursor()
        cursor.execute('''select ora,mera,onoma,eponimo
                        from (didaskalia join PRAGMATOPOIEI on epipedo_did=epipedo and etos_did=etos and noumero_did=noumero) join PROSOPIKO  on kodikos=kodikos_prop
                        where epipedo=? and etos=? and noumero=?''',[epipedo,etos,noumero])
        data=cursor.fetchall()
        return data

    @staticmethod
    def find_plirofories_gipedou(conn,arithmos):
        cursor=conn.cursor()
        cursor.execute('''select eidos_gipedou,dieuthinsi,kostos_aneks_kratisis from gipedo where arithmos_gipedou=?''',[arithmos])
        data=cursor.fetchall()
        return data[0][0],data[0][1],data[0][2]

    @staticmethod
    def find_onomateponima_proponiton(conn):
        cursor=conn.cursor()
        cursor.execute('''select eponimo,onoma from prosopiko natural join proponitis''')
        data=cursor.fetchall()
        return data

    @staticmethod
    def find_tilefono_prosopikou(conn,onoma,eponimo):
        cursor=conn.cursor()
        cursor.execute('''select tilefono from prosopiko where onoma=? and eponimo=?''',[onoma,eponimo])
        data=cursor.fetchall()
        return Utility.extract_one_tuple_value(data)

    @staticmethod
    def find_kostos_idiaiterou(conn,onoma,eponimo,tilefono):
        cursor=conn.cursor()
        cursor.execute('''select kostos_mathimatos from proponitis natural join prosopiko where onoma=? and eponimo=? and tilefono=?''',[onoma,eponimo,tilefono] )
        data=cursor.fetchall()
        return Utility.extract_one_tuple_value(data)[0]

    @staticmethod
    def find_kodikos_proponiti(conn,onoma,eponimo,tilefono):
        cursor=conn.cursor()
        cursor.execute('''select kodikos from proponitis natural join prosopiko where onoma=? and eponimo=? and tilefono=?''',[onoma,eponimo,tilefono] )
        data=cursor.fetchall()
        return Utility.extract_one_tuple_value(data)[0]

    @staticmethod
    def find_tilefona_melous(conn,onoma,eponimo):
        cursor=conn.cursor()
        cursor.execute('''select tilefono from melos where onoma=? and eponimo=?''',[onoma,eponimo] )
        data=cursor.fetchall()
        return Utility.extract_one_tuple_value(data)

    @staticmethod
    def find__melontikes_kratisis_mias_didaskalias(conn,epipedo,etos,noumero):
        cursor=conn.cursor()
        cursor.execute('''  select imerominia,ora,arithmos_gipedou,dieuthinsi
                            from (DIMIOURGEI join KRATISI on kodikos_krat=kodikos ) natural join gipedo
                            where epipedo=? AND etos=? and noumero_did=? and imerominia>=date() and anablithike=false
                            order by imerominia''',[epipedo,etos,noumero] )
        data=cursor.fetchall()
        return data


    @staticmethod
    def find_kratisis_didaskalion_gia_proponiti(conn,kodikos,imerominia):
        # Ginetai join pragmatopoiei,dimiourgei,kratisi,gipedo. Epistrefei gia enan proponiti tis kratisis mathimaton tou oi opoies ginontai apo tin imerominia kai meta


        cursor=conn.cursor()
        cursor.execute('''  select k.kodikos,k.imerominia,k.ora,k.arithmos_gipedou,g.dieuthinsi
                            from PRAGMATOPOIEI as p, DIMIOURGEI d, kratisi k,gipedo g
                            where p.epipedo_did=d.epipedo  and p.etos_did=d.etos and p.noumero_did=d.noumero_did
                            and k.kodikos=d.kodikos_krat and g.arithmos_gipedou=k.arithmos_gipedou and p.ora=k.ora and p.kodikos_prop=? and k.imerominia>=? and anablithike=false
							and p.mera=(select case  strftime('%w', k.imerominia) 
										  when '0' then 'ΚΥΡΙΑΚΗ'
										  when '1' then 'ΔΕΥΤΕΡΑ'
										  when '2' then 'ΤΡΙΤΗ'
										  when '3' then 'ΤΕΤΑΡΤΗ'
										  when '4' then 'ΠΕΜΠΤΗ'
										  when '5' then 'ΠΑΡΑΣΚΕΥΗ'
										  else 'ΣΑΒΒΑΤΟ' end as servdayofweek);  ''',[kodikos,imerominia] )
        data=cursor.fetchall()
        # Xoris to case epistrefei tis kratisis ton group sta opoia didaskei o zitoumenos proponitis. Apo oles tis kratisis prepei na kratisoume mono autes pou antistoixoun
        # stis meres didaskalias tou
        return data
    
    @staticmethod
    def find_plirofories_proponiton(conn):
        cursor=conn.cursor()
        cursor.execute('''select eponimo,onoma,tilefono from prosopiko natural join proponitis order by eponimo''')
        data=cursor.fetchall()
        return data

    @staticmethod
    def find_plirofories_melon(conn):
        cursor=conn.cursor()
        cursor.execute('''select onoma,eponimo,tilefono from melos''' )
        data=cursor.fetchall()
        return data

class Simulate():
    ''' Γεμίζει όλους τους πίνακες με έγκυρα δεδομένα'''

    def __init__(self):
        self.empty_data_base()
        a=atomoCreator()
        random.seed(7)          #400,40,30,10,1000,100
        a.fill_atomo(100,'melos')
        a.fill_atomo(30,'prosopiko')
        self.assign_roles()
        self.fill_matihmata()
        self.fill_gipedo(10)
        self.assign_sintirites()
        self.fill_didaskalies(40)
        self.fill_orario_proponiton()
        self.anathese_didaskalies_se_proponites()
        self.fill_kratisis_didaskalion('2023-09-01','2024-03-31')
        self.assign_meli_to_didaskalies()
        self.fill_kanei(100)
        self.fill_eksoflei()
        self.fill_plironei()
        self.fill_anaplironei(50)
        
    def assign_roles(self):
        
        conn=Utility.create_connection()
        kodikoi_prosopikou=Sql.find_kodikous_of_all_prosopiko(conn)
        Sql.insert_grammatea(conn,kodikoi_prosopikou[0],1000)  #Iparxei toylaxiston mia gramatia

        for kodiko in kodikoi_prosopikou[1:]: 

            epiloges = [1, 2, 3]                  #1: proponitis, 2:sintiritis, 3:grammateas
            weights = [0.85, 0.1, 0.05]

            choice=random.choices(epiloges, weights)[0]
            
            if (choice==1): Sql.insert_proponiti(conn,kodiko)
            elif (choice==2): Sql.insert_sintiriti(conn,kodiko,900)
            else: Sql.insert_grammatea(conn,kodiko,1000)

        conn.close()

    def empty_data_base(self):
        # SYMMETEXEI, KANEI
        tables=['PRAGMATOPOIEI','PROSOPIKO','MELOS','MATHIMA','DIDASKALIA','PROPONITIS_ORARIO','KRATISI','GIPEDO','DIMIOURGEI','ANAPLIRONEI','MELOS','SYMMETEXEI','KANEI','PLIROMI','PLIRONEI','EKSOFLEI']
        conn=Utility.create_connection()

        for pinaka in tables: Sql.empty_table(conn,pinaka)
        conn.close()

    def fill_matihmata(self):
        mathimata=[('ΑΡΧΑΡΙΟΙ',2),('ΜΕΤΡΙΟΙ',3),('ΠΡΟΧΩΡΗΜΕΝΟΙ',4)]
        conn=Utility.create_connection()

        for mathima in mathimata:
            epipedo=mathima[0]
            ores=mathima[1]
            Sql.insert_mathima(conn,epipedo,ores)

        conn.close()

    def fill_gipedo(self,number):
        dieuthinsis=[]
        self.read_dieuthinsis_gipedou(dieuthinsis)
        dinata_idoi=["ΣΚΛΗΡΟ","ΧΩΜΑΤΙΝΟ","ΜΟΚΕΤΑ","ΓΡΑΣΙΔΙ","ΚΛΕΙΣΤΟ"]
        weights = [0.25, 0.1, 0.3, 0.3, 0.05 ]
        conn=Utility.create_connection()

        for i in range(number):
            
            idos=random.choices(dinata_idoi, weights)[0]
            dieuthinsi= dieuthinsis[ ran( 0,len(dieuthinsis)-1) ]
            Sql.insert_gipedo(conn,idos,dieuthinsi)

        conn.close()

    def read_dieuthinsis_gipedou(self,dieuthinsis):
        path_python= os.path.dirname(__file__)
        path_dieuthinsis_gipedon=  os.path.join(path_python,"arxia_gia_prosomiosi","dieuthinsis.txt")
        Utility.read_file(path_dieuthinsis_gipedon,dieuthinsis)

    @staticmethod       #Xrisimopoieitai kai apo ali klasi
    def create_ilikiako_euros():
        epiloges = ['ΚΑΤΩ ΤΩΝ 10','10-12','13-15','16-17','ΕΝΗΛΙΚΑΣ']                 
        weights = [0.2,0.2,0.2,0.2,0.2]

        choice=random.choices(epiloges, weights)[0]
        return choice

    def fill_didaskalies(self,number):
        conn=Utility.create_connection()
        dinata_epipeda= Sql.find_dinata_epipeda(conn)[0]

        for i in range(number):

            #change
            epipedo= dinata_epipeda[ ran(0,len(dinata_epipeda)-1) ]
            etos='2023-2024'
            ilikiako_euros=self.create_ilikiako_euros()

            if(epipedo=='ΑΡΧΑΡΙΟΙ'): kostos=30
            elif(epipedo=='ΜΕΤΡΙΟΙ'): kostos=40
            elif(epipedo=='ΠΡΟΧΩΡΗΜΕΝΟΙ'): kostos=50
            else: kostos=30

            res= Sql.find_megalitero_noumero_epipedou(conn,etos,epipedo)    # An den iparxei epistrefei None
            if res==None: noumero=1
            else: noumero=res+1
            Sql.insert_didaskalia(conn,epipedo,etos,noumero,kostos,ilikiako_euros)

        conn.close()

    def fill_orario_proponiton(self):

        conn=Utility.create_connection()
        kodikoi_proponiton=Sql.find_kodikous_proponiton(conn)
        dinates_meres=["ΔΕΥΤΕΡΑ","ΤΡΙΤΗ","ΤΕΤΑΡΤΗ","ΠΕΜΠΤΗ","ΠΑΡΑΣΚΕΥΗ","ΣΑΒΒΑΤΟ","ΚΥΡΙΑΚΗ"]

        # Einai anoixto to tenis club apo tis 8 to proi mexri tis 12 to bradi
        endeiktika_oraria=[('09:00-13:00', '16:00-22:00'), ('09:00-17:00'), ('10:00-14:00', '17:00-22:00'),('17:00-24:00'),None]
        

        for kodikos in kodikoi_proponiton:
        
            for mera in dinates_meres:
                orario=endeiktika_oraria[ran(0,len(endeiktika_oraria)-1)]
                if orario!=None:
                    if(isinstance(orario,str)):             #Periexei mono mia timi
                        Sql.insert_orario(conn,kodikos,orario,mera)
                    else:
                        for ores in orario:
                            Sql.insert_orario(conn,kodikos,ores,mera)
        conn.close()

    def anathese_didaskalies_se_proponites(self):
        conn=Utility.create_connection()
        #change
        didaskalies=Sql.find_didaskalies(conn,'2023-2024')

        for didaskalia in didaskalies:
            (epipedo,etos,noumero,kostos,ilikiako_euros)=didaskalia

            fores=Sql.find_ebdomadiaies_ores_mathimatos(conn,epipedo)
            for i in range(int(fores)):
                kodikos_proponiti,ora_int,lepta_int,mera= Utility.find_diathesimi_ora_kai_proponiti(conn,1,0)

                while(Sql.checkIfMathimaAlreadyExistsForADay(conn,epipedo,etos,noumero,mera)):
                            kodikos_proponiti,ora_int,lepta_int,mera= Utility.find_diathesimi_ora_kai_proponiti(conn,1,0)

                
                ora_string=Utility.convert_ora(ora_int,lepta_int)
                Sql.insert_pragmatopoiei(conn,kodikos_proponiti,epipedo,etos,noumero,ora_string,mera)

        conn.close()
    
    def fill_kratisis_didaskalion(self,start_date,end_date):
        #p.x. start_date='2023-09-01' kai end_date='2024-08-31'
        #etos='2023-2024'

        conn=Utility.create_connection()
        etos=start_date[0:4]+'-'+end_date[0:4]
        didaskalies=Sql.find_didaskalies(conn,etos)

        for didaskalia in didaskalies:
            (epipedo,etos,noumero,kostos,ilikiako_euros)=didaskalia
            Utility.dimiourgia_kratiseon_gia_didaskalia(conn,epipedo,etos,noumero,start_date,end_date,None)
        
        conn.close()


    def assign_sintirites(self):
        conn=Utility.create_connection()
        kodikoi_sintiriton=Sql.find_kodikous_sintiriton(conn)
        arithmoi_gipedon=Sql.find_kodikous_gipedon(conn)

        for gipedo in arithmoi_gipedon:
            num=ran(0,len(kodikoi_sintiriton)-1)
            sintiritis=kodikoi_sintiriton[num]
            Sql.update_sintiriti_gipedou(conn,sintiritis,gipedo)
        conn.close()

    def create_imerominia(self,start_date,end_date):
        # epistrefei mia imerominia sto diastima [start_date, end_date]

        year_start,month_start,day_start= Utility.break_strDate_to_integers(start_date)
        year_end,month_end,day_end= Utility.break_strDate_to_integers(end_date)

        start_date = datetime.date(year_start, month_start, day_start)
        end_date   = datetime.date(year_end, month_end, day_end)
        if(start_date!=end_date):
            num_days   = (end_date - start_date).days
            rand_days   = random.randint(1, num_days)
            random_date = start_date + datetime.timedelta(days=rand_days)
            return str(random_date)
        else:
            return str(start_date)

    def assign_meli_to_didaskalies(self):
        conn=Utility.create_connection()
        kodikoi_melon_kai_ilikiako_euros=Sql.find_kodikous_melon_kai_ilikiako_euros(conn)
        #change
        didaskalies=Sql.find_didaskalies(conn,'2023-2024')
        for kataxorisi in kodikoi_melon_kai_ilikiako_euros:
            kodikos=kataxorisi[0]
            ilikiako_euros_melous=kataxorisi[1]

            assign=ran(0,2)    # An assign=0 den ton anatheti se kapoia didaskalia , an assign =2 ton anatheti se  2...
            
            if(assign!=0):
                
                for didaskalia in didaskalies:
                    
                    epipedo,etos,noumero,miniaio_kostos,ilikiako_euros_didaskalias=didaskalia
                    if(ilikiako_euros_didaskalias==ilikiako_euros_melous):
                        if(not Elegxoi.check_if_didaskalia_is_full(conn,epipedo,etos,noumero)):
                            if(not Elegxoi.check_melos_idi_simetexei_se_didaskalia(conn,kodikos,epipedo ,etos,noumero)):
                                imerominia_enarksis=self.create_imerominia('2023-09-01','2023-11-30')
                                Sql.insert_symetexei(conn,kodikos,epipedo,etos,noumero,imerominia_enarksis)
                                assign -=1

                                unassign=ran(0,4)   # Me pithanotita 1/5  ton appegrafi apo tin didaskalia
                                if(unassign==0):
                                    imerominia_liksis=self.create_imerominia(imerominia_enarksis,'2023-12-17')
                                    Sql.appegrafi_from_symetexei(conn,kodikos,epipedo,etos,noumero,imerominia_enarksis,imerominia_liksis)
                    if(assign==0): break
        
        conn.close()

    def fill_kanei(self,kratisis):
        conn=Utility.create_connection()
        kodikoi_melon=[]
        kodikoi_melon_kai_ilikiako_euros=Sql.find_kodikous_melon_kai_ilikiako_euros(conn)
        for kataxorisi in kodikoi_melon_kai_ilikiako_euros:
            kodikos=kataxorisi[0]
            kodikoi_melon.append(kodikos)



        while(kratisis>0):
            today=Utility.find_current_date()
            kodikos_proponiti,ora_int,lepta_int,mera=Utility.find_diathesimi_ora_kai_proponiti(conn,1,0)   # O proponitis pou epistrefetai den exei ali didaskalia

            aneksartiti_kratisi=ran(0,2) #Ean aneksarti_kratisi==1 , tote ginetai kratisi gipedou xoris proponiti
            if(aneksartiti_kratisi==1): kodikos_proponiti=None

            mera_int=Utility.convert_weekday_to_weekdayInt(mera)
            imerominia=Utility.find_all_dates(today,'2034-10-30',mera_int)[0]
            ora=Utility.convert_ora(ora_int,lepta_int)
            kodikoi_gipedon=Sql.find_kodikous_gipedon(conn)
            gipedo=kodikoi_gipedon[ran(0,len(kodikoi_gipedon)-1)]
            melos=kodikoi_melon[ran(0,len(kodikoi_melon)-1)]
            if(Utility.dimiourgia_ksexoristis_kratisis(conn,imerominia,ora,gipedo,melos,kodikos_proponiti)): kratisis -=1

        conn.close()

    def fill_eksoflei(self):
        conn=Utility.create_connection()
        kodikoi_melous=Sql.find_kodikous_melon(conn)
        for kodiko in kodikoi_melous:
            #change
            didaskalies_melous=Sql.find_didaskalies_pou_simmetexei_ena_atomo_gia_ena_xrono(conn,kodiko,'2023-2024')
            for didaskalia in didaskalies_melous:
                kod,epipedo,etos,noumero,imerominia_enarksis,imerominia_liksis=didaskalia
                poso=Sql.find_kostos_didaskalias(conn,epipedo,etos,noumero)

                mines_pou_prepei_na_plirosi=Utility.find_aplirotous_mines_gia_mia_didaskalia_gia_ena_atomo(conn,kod,epipedo,etos,noumero,imerominia_enarksis,imerominia_liksis)

                for mina in mines_pou_prepei_na_plirosi:
                    etos_pliromis=self.find_etos(mina)
                    mina_int=Utility.antistoixise_mina_se_noumero(mina)
                    day=ran(0,28)
                    imerominia_pliromis=Utility.format_date(etos_pliromis,mina_int,day)
                    pithanotita=ran(0,7)  # Plironetai to 1/8 to kratiseon
                    if(pithanotita!=0):
                        Utility.pliromi_didaskalias(conn,imerominia_pliromis,kodiko,epipedo,etos,noumero,mina)
        conn.close()

    def find_etos(self,minas):
        #change
        "Gia to simulation ean o minas einai septembrios mexri dekembrios etos=2023 alios 2024"
        mines_2023=['ΣΕΠΤΕΜΒΡΙΟΣ','ΟΚΤΩΒΡΙΟΣ','ΝΟΕΜΒΡΙΟΣ','ΔΕΚΕΜΒΡΙΟΣ']
        if minas in mines_2023: return 2023
        else: return 2024

    def fill_plironei(self):
        #change
        conn=Utility.create_connection()
        kodikoi_atomon=Sql.find_kodikous_melon(conn)
        pliromi_kratiseon_prin_apo_mera='2024-01-15'
        for kodiko_melous in kodikoi_atomon:

            aneksartites_kratisis= Sql.find_aplirotes_kratisis_atomou_gia_mia_imerominia_kai_prin(conn,kodiko_melous,pliromi_kratiseon_prin_apo_mera)
            for kratisi in aneksartites_kratisis:

                a=ran(0,1)
                if(a==1):
                    imerominia_kratisis=Sql.find_imerominia_dieuthinsi_gipedou_kai_arithmo_gipedou_gia_kratisi(conn,kratisi)[0]
                    imerominia_pliromis=self.create_imerominia(imerominia_kratisis,'2024-01-14')
                    Utility.pliromi_kratisis(conn,imerominia_pliromis,kratisi,kodiko_melous)

        conn.close()

    def fill_anaplironei(self,num):

        conn=Utility.create_connection()
        kratisis=Sql.find_melontikous_kodikous_kratiseon_pou_antistoixoun_se_didaskalies(conn)
        kodikoi_proponiton=Sql.find_kodikous_proponiton(conn)
        
        for i in range (num):

            kratisi=Sql.find_kratisi(conn,kratisis[i])
            
            kodikos_arxikis_krat=kratisi[0]
            imerominia=kratisi[1]
            mera=Utility.convert_dateObject_to_weekday(Utility.convert_date_to_dateObject(imerominia))
            ora=kratisi[2]
            arithmos_gipedou=kratisi[4]
            Sql.anaboli_sigkekrimenis_kratisis(conn,kodikos_arxikis_krat)

            for kodiko in kodikoi_proponiton:

                anaplirosis_temp=Sql.find_melontikes_anaplirosis_proponiti(conn,kodiko)
                ksexoristes_kratisis_temp=Sql.find_melontikes_aneksartites_kratisis_proponiti(conn,kodiko)

                anaplirosis=Utility.extract_sec_and_third_values_from_list_of_tuples(anaplirosis_temp)
                ksexoristes_kratisis=Utility.extract_sec_and_third_values_from_list_of_tuples(ksexoristes_kratisis_temp)
                
                if(Elegxoi.check_if_proponitis_is_available(conn,kodiko,ora,mera,imerominia,ksexoristes_kratisis,anaplirosis)[0]):
                    if(Elegxoi.check_if_gipedo_is_available(conn,arithmos_gipedou,imerominia,ora,1,0)):
                        Sql.insert_kratisi(conn,imerominia,ora,arithmos_gipedou)
                        kodikos_neas_kratisis=Sql.find_kodikos_proigoumenis_isaxthisas_timis_pinaka(conn,'KRATISI')
                        Sql.insert_anaplironei(conn,kodiko,kodikos_arxikis_krat,kodikos_neas_kratisis)
                        break
        conn.close()

class Query():
    '''Περιέχει συναρτήσεις που χρησιμοποιεί το Gui. Μορφοποιούν κατάλληλα τα δεδομένα για να είναι έτοιμα προς παρουσίαση'''

    @staticmethod
    def find_kratisis_kai_didaskalies_pou_exei_kai_den_exei_plirosi_ena_atomo(onoma,eponimo,tilefono):
        # Epistrefei tis pliromenes_kratisis,aplirotes_kratisis,pliromenes_didaskalies,aplirotes_didaskalies

        conn=Utility.create_connection()
        kodikos_atomou=Sql.find_kodikos_melous(conn,onoma,eponimo,tilefono)

        pliromenes_kratisis=Sql.find_pliromenes_kratisis_atomou(conn,kodikos_atomou)
        aplirotes_kratisis=Sql.find_aplirotes_kratisis_atomou_gia_mia_imerominia_kai_prin(conn,kodikos_atomou,Utility.find_date_of_next_year())

        # kodikos kratisis, imerominia, onoma proponiti, eponimo proponiti, dieuthinsi gipedou, arithmos gipedou , kostos
        res_pliromenes_kratisis=Query.format_kratisi(conn,pliromenes_kratisis)
        res_aplirotes_kratisis=Query.format_kratisi(conn,aplirotes_kratisis)
        aplirotes_didaskalies,pliromenes_didaskalies=Utility.find_aplirotes_kai_pliromenes_didaskalies_atomou(conn,kodikos_atomou,Utility.find_current_year_period())

        conn.close()

        return res_pliromenes_kratisis,res_aplirotes_kratisis,pliromenes_didaskalies,aplirotes_didaskalies

    @staticmethod
    def format_kratisi(conn,kratisis):

        res=[]

        for kratisi in kratisis:

            onoma,eponimo= Sql.find_onomateponimo_proponiti_pou_ekane_idiaitero(conn,kratisi)
            imerominia,dieuthinsi,arithmos_gipedou,ora= Sql.find_imerominia_dieuthinsi_gipedou_kai_arithmo_gipedou_gia_kratisi(conn,kratisi)
            kostos=Sql.find_kostos_aneksartitis_kratisis(conn,kratisi)
            res.append((kratisi,imerominia,ora,onoma,eponimo,dieuthinsi,arithmos_gipedou,kostos))
        
        return res

    @staticmethod
    def format_didaskalies(ilikiako_euros):
        conn=Utility.create_connection()
        etos=Utility.find_current_year_period()
        data=Sql.find_mi_gemata_group_gia_ilikiako_euros(conn,etos,ilikiako_euros)
        res=[]
        for kataxorisi in data:
            epipedo,etos,noumero,miniaio_kostos,ilikiako_euros,simetexontes=kataxorisi
            ora_mera_kai_onomateponimo_proponiton=Sql.find_ora_mera_kai_onomateponimo_proponiti_gia_didaskalia(conn,epipedo,etos,noumero)
            res.append((epipedo,etos,noumero,ilikiako_euros,miniaio_kostos,ora_mera_kai_onomateponimo_proponiton))

        conn.close()

        return res

    @staticmethod
    def find_piasmenes_ores_proponiti_gia_imerominia(kodiko,imerominia):
        conn=Utility.create_connection()
        anaplirosis=Sql.find_melontikes_anaplirosis_proponiti(conn,kodiko)
        ksexoristes_kratisis=Sql.find_melontikes_aneksartites_kratisis_proponiti(conn,kodiko)  #kodikos, imerominia,ora
        today=Utility.find_current_date()
        kratisis_mathimaton=Sql.find_kratisis_didaskalion_gia_proponiti(conn,kodiko,today)
        kratisis=anaplirosis+ksexoristes_kratisis+kratisis_mathimaton
        ora_kratiseon=[]
        for kataxorisi in kratisis:
            imer=kataxorisi[1]
            ora=kataxorisi[2]
            if(imer==imerominia):
                ora_kratiseon.append(ora)
        ora_kratiseon.sort()
        conn.close()
        return ora_kratiseon

    @staticmethod
    def find_orario_proponiti_gia_mia_mera(conn,kodikos,mera):
        orario=Sql.find_orario_proponiti(conn,kodikos)
        res=[]
        for kataxorisi in orario:
            ora_prop,mera_prop=kataxorisi
            if(mera_prop==mera):
                res.append(ora_prop)
        return res

class Gui():

    '''Γραφική διεπαφή'''

    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry('1000x800')
        self.root.resizable(False, False)
        self.root.title('Tennis club')

        self.create_initial_menu() 
        self.conn=Utility.create_connection()
        self.root.mainloop()      

    def format_string(self,stra):
        
        #Αφαιρει τονους, αλλάζει το ς->σ κτλ.

        d = {ord('\N{COMBINING ACUTE ACCENT}'):None}
        g=ud.normalize('NFD',stra).translate(d)
       
        return g.upper()

    def format_tilefono(self,tilefono):
        return tilefono.replace('-','')

    def create_initial_menu(self):
        self.frame0= tk.Frame(self.root,bg='#FAEED1')
        self.frame0.pack(fill='both', expand=True)
        b1=tk.Button(self.frame0,text='PAYMENT',bg='#EAD196',command= self.create_menu_pliromis,width=24,height=10)
        b1.place(x=120,y=50)

        b2=tk.Button(self.frame0,text='LESSON SIGNUP',bg='#EAD196',command= self.create_menu_eggrafis_se_didaskalia,width=24,height=10)
        b2.place(x=420,y=50)

        b3=tk.Button(self.frame0,text='RESERVATION',bg='#EAD196',command= self.create_menu_kratiseon,width=24,height=10)
        b3.place(x=720,y=50)

        b4=tk.Button(self.frame0,text='NEW MEMBER',bg='#EAD196',command= self.create_menu_eggrafis_melon,width=24,height=10)
        b4.place(x=120,y=300)

        b5=tk.Button(self.frame0,text='INSTRUCTOR COURSES',bg='#EAD196',command= self.create_menu_mathimaton_proponiton,width=24,height=10)
        b5.place(x=420,y=300)

        b6=tk.Button(self.frame0,text='COURSE RESERVATIONS',bg='#EAD196',command= self.create_menu_kratisis_didaskalion,width=24,height=10)
        b6.place(x=720,y=300)

    def create_menu_pliromis(self):
        w = tk.Toplevel(self.frame0)
        w.geometry('1000x800')
        w.resizable(False, False)

        onoma_eponimo_tilefono_melon_temp2=Sql.find_plirofories_melon(self.conn)
        onoma_eponimo_tilefono_melon_temp1=[]
        
        for kataxorisi in onoma_eponimo_tilefono_melon_temp2:
            onoma=kataxorisi[0]
            eponimo=kataxorisi[1]
            tilefono=str(kataxorisi[2])
            tilefono='('+tilefono+')'
            onoma_eponimo_tilefono_melon_temp1.append((eponimo,onoma,tilefono))

        onoma_eponimo_tilefono_melon= sorted(onoma_eponimo_tilefono_melon_temp1, key=lambda tup: tup[0])   # taksinomisi me basi to eponimo


        combo1 = ttk.Combobox(w,state="readonly", values=onoma_eponimo_tilefono_melon,width=50)
        combo1.grid(row=0,column=1)

        l1=tk.Label(w,text='MEMBER:')
        l1.grid(row=0,column=0,padx=5)

        f1=tk.Frame(w,bg='red')
        f2=tk.Frame(w,bg='blue')
        l4=tk.Label(w,text='RESERVATIONS')
        l5=tk.Label(w,text='COURSES')

        l4.grid(row=4,column=1)
        l5.grid(row=4,column=24)
        w.grid_columnconfigure(28, minsize=100)


        f1.grid(row=5,column=0,pady=10,padx=10,columnspan=15)
        f1.config(width=480,height=550)
        f2.grid(row=5,column=14,pady=10,padx=10,columnspan=15)
        f2.config(width=420,height=550)


        self.kodikos_kratisis=-1
        self.epipedo=-1
        self.etos=-1
        self.noumero=-1
        self.minas=-1

        def get_values_from_menu_pliromis():
            res=combo1.get()
            if(res==''):return False

            eponimo,onoma,tilefono=res.split(' ')
            tilefono=tilefono.replace('(',"")
            tilefono=tilefono.replace(')',"")
            
            return onoma,eponimo,tilefono

        def fill_table(*args):

            tree.delete(*tree.get_children())
            tree2.delete(*tree2.get_children())

            if(not get_values_from_menu_pliromis()):
                return
            onoma,eponimo,tilefono=get_values_from_menu_pliromis()
            tilefono=int(tilefono)
            plir_aplir=menu_str.get()
            
            if(not Elegxoi.melosExists(onoma,eponimo,tilefono)):
                tk.messagebox.showerror("Not found", "Member not found",parent=w)
                return

            pliromenes_kratisis,aplirotes_kratisis,pliromenes_didaskalies,aplirotes_didaskalies=Query.find_kratisis_kai_didaskalies_pou_exei_kai_den_exei_plirosi_ena_atomo(onoma,eponimo,tilefono)
            if (plir_aplir=='PAID'):
                b2.grid_forget()

                kratisis=pliromenes_kratisis
                didaskalies=pliromenes_didaskalies
            elif(plir_aplir=='UNPAID'):
                b2.grid(row=0,column=28)

                kratisis=aplirotes_kratisis
                didaskalies=aplirotes_didaskalies
            if (kratisis!=None):
                for kataxorisi in kratisis:
                    kodikos_krat,imerominia,ora,onoma_prop,eponimo_prop,dieuth,arithmos_gip,kostos=kataxorisi
                    if(onoma_prop==None):onoma_prop=''
                    if(eponimo_prop==None):eponimo_prop=''

                    tree.insert("","end",values = (kodikos_krat,imerominia,ora,onoma_prop,eponimo_prop,dieuth,arithmos_gip,kostos))

            if (didaskalies!=None):
                for kataxorisi in didaskalies:
                    epipedo,etos,noumero,minas,poso=kataxorisi
                    tree2.insert("","end",values = (epipedo,etos,noumero,minas,poso))

        combo1.bind("<<ComboboxSelected>>", fill_table)
        
        OPTIONS = ["PAID",'UNPAID']

        menu_str = tk.StringVar(master=w) 
        menu_str.set(OPTIONS[0]) 
        menu_str.trace("w", fill_table)

        drop_down = tk.OptionMenu(w, menu_str, *OPTIONS)
        drop_down.config(width = 20)
        drop_down.grid(row=0,column=3)


        def pliromi():
            imerominia=Utility.find_current_date()
            onoma,eponimo,tilefono=get_values_from_menu_pliromis()
            kodikos_atomou=Sql.find_kodikos_melous(self.conn,onoma,eponimo,tilefono)

            if(self.kodikos_kratisis==-1): #Exei epilegei didaskalia
                Utility.pliromi_didaskalias(self.conn,imerominia,kodikos_atomou,self.epipedo,self.etos,self.noumero,self.minas)
                fill_table()
                

            if(self.epipedo==-1):  #Exei epilegei kratisi
                Utility.pliromi_kratisis(self.conn,imerominia,self.kodikos_kratisis,kodikos_atomou)

                fill_table()



        b2=tk.Button(w,text='PAY',command=pliromi)
        b2.grid(row=0,column=10)
        b2.grid_forget()

        tree = ttk.Treeview(f1, columns=("size", "modified"))
        tree["columns"] = ("code", "date","hour", "inst name","inst surname", "course addr", "course num","cost")

        tree.column("code", width=50)
        tree.column("date", width=50)
        tree.column("hour", width=65)

        tree.column("inst name", width=60)
        tree.column("inst surname", width=60)
        tree.column("course addr", width=60)
        tree.column("course num", width=50)
        tree.column("cost", width=40)

        tree.column('#0',width=0,stretch=0)
        tree.heading("code", text="code")
        tree.heading("date", text="date.")
        tree.heading("hour", text="hour")
        tree.heading("inst name", text="inst name")
        tree.heading("inst surname", text="inst surname")
        tree.heading("course addr", text="course addr")
        tree.heading("course num", text="course num")
        tree.heading("cost", text="cost")

        tree2 = ttk.Treeview(f2, columns=("size", "modified"))
        tree2["columns"] = ("level", "year", "number","month", "amount")

        tree2.column("level", width=40)
        tree2.column("year", width=30)
        tree2.column("number", width=30)
        tree2.column("month", width=50)
        tree2.column("amount", width=40)

        tree2.column('#0',width=0,stretch=0)
        tree2.heading("level", text="level")
        tree2.heading("year", text="year.")
        tree2.heading("number", text="number")
        tree2.heading("month", text="month")
        tree2.heading("amount", text="amount")

        def selectItem(a):
            self.epipedo=-1
            self.etos=-1
            self.noumero=-1
            self.minas=-1
            curItem = tree.focus()
            leks=tree.item(curItem)
            try:
                self.kodikos_kratisis=leks['values'][0]
            except:
                pass

        def selectItem2(a):
            self.kodikos_kratisis=-1
            curItem = tree2.focus()
            leks=tree2.item(curItem)
            self.epipedo=leks['values'][0]
            self.etos=leks['values'][1]
            self.noumero=leks['values'][2]
            self.minas=leks['values'][3]

        tree.bind('<ButtonRelease-1>', selectItem)
        tree.place(width=480,height=550)

        tree2.bind('<ButtonRelease-1>', selectItem2)
        tree2.place(width=420,height=550)
        
    def create_menu_eggrafis_se_didaskalia(self):
        w = tk.Toplevel(self.frame0)
        w.geometry('1400x800')
        w.resizable(False, False)
        tree = ttk.Treeview(w, columns=("size", "modified"))
        tree["columns"] = ("level", "year", "number", "year range","cost", "hour-day-inst name")

        tree.column("level", width=20)
        tree.column("year", width=20)
        tree.column("number", width=20)
        tree.column("year range", width=20)
        tree.column("cost", width=20)
        tree.column("hour-day-inst name", width=300)

        tree.column('#0',width=0,stretch=0)
        tree.heading("level", text="level")
        tree.heading("year", text="year.")
        tree.heading("number", text="number")
        tree.heading("year range", text="year range")
        tree.heading("cost", text="cost")
        tree.heading("hour-day-inst name", text="hour-day-inst name")
        
        self.epipedo=-1
        self.etos=-1
        self.noumero=-1

        def selectItem(a):
            curItem = tree.focus()
            leks=tree.item(curItem)
            self.epipedo=leks['values'][0]
            self.etos=leks['values'][1]
            self.noumero=leks['values'][2]

        def fill_table():
            ilikiako_euros=menu_str.get()
            if(ilikiako_euros!='year range'):
                tree.delete(*tree.get_children())
                didaskalies=Query.format_didaskalies(ilikiako_euros)
                for kataxorisi in didaskalies:
                    epipedo,etos,noumero,ilikiako_euros,kostos,ora_mera_onomateponimo_proponiton=kataxorisi
                    tree.insert("","end",values = (epipedo,etos,noumero,ilikiako_euros,kostos,ora_mera_onomateponimo_proponiton))


        tree.bind('<ButtonRelease-1>', selectItem)
        tree.place(width=1240,height=750)

        menu_str= tk.StringVar(w)
        menu_str.set('year range')
        drop_down=tk.OptionMenu(w,menu_str,'under 10','10-12','13-15','16-17','adult')
        drop_down.grid(row=3,column=1)
        drop_down.place(x=1250)

        b1=tk.Button(w,text='submit',command=fill_table)
        b1.place(x=1250,y=50,height=40)

        

        def eggrafi():
            if (self.epipedo!=-1):
                create_parathiro_eggrafis()

        b2=tk.Button(w,text='JOIN',command=eggrafi)
        b2.place(x=1250,y=100,height=50)

        def create_parathiro_eggrafis():
            w2 = tk.Toplevel(w)
            w2.geometry('400x400')
            w2.resizable(False, False)
            l1=tk.Label(w2,text='NAME:')
            l1.place(x=20,y=20,height=30)
            e1=tk.Entry(w2)
            e1.place(x=120,y=20,height=30)
            
            l2=tk.Label(w2,text='LAST NAME:')
            l2.place(x=20,y=60,height=30)
            e2=tk.Entry(w2)
            e2.place(x=120,y=60,height=30)

            l3=tk.Label(w2,text='PHONE:')
            l3.place(x=20,y=100,height=30)
            e3=tk.Entry(w2)
            e3.place(x=120,y=100,height=30)

            def eggrafi_melous():
                onoma=self.format_string(e1.get())
                eponimo=self.format_string(e2.get())
                tilefono=int(self.format_tilefono(e3.get()))
                
                if(Elegxoi.melosExists(onoma,eponimo,tilefono)):
                    imerominia=Utility.find_current_date()
                    kodikos_melous=Sql.find_kodikos_melous(self.conn,onoma,eponimo,tilefono)
                    Sql.insert_symetexei(self.conn,kodikos_melous,self.epipedo,self.etos,self.noumero,imerominia)
                    self.epipedo=-1
                    l4=tk.Label(w2,text="Successful sign up")
                    l4.place(x=180,y=350,height=30)

                else:
                    tk.messagebox.showerror("Not found", "Member not found",parent=w2)
                

            b=tk.Button(w2,text='JOIN',command=eggrafi_melous)
            b.place(x=300,y=330,height=50)

    def create_menu_kratiseon(self):
        w = tk.Toplevel(self.frame0)
        w.geometry('1000x800')
        w.resizable(False, False)


        def create_imerominies_epomenon_efta_imeron():
            today=Utility.find_current_date()
            today_int=Utility.convert_weekday_to_weekdayInt(Utility.convert_dateObject_to_weekday(Utility.convert_date_to_dateObject(today)))
            res=[]
            for i in range (1,8):
                next_day=(today_int+i)%7
                if(next_day!=today_int):
                    res.append(Utility.find_all_dates(today,'2034-10-01',next_day)[0])
                else:
                    res.append(Utility.find_all_dates(today,'2034-10-01',next_day)[1])
            return res

        def fill_tables(a):
            date=combo1.get()
            if(date!=''):
                fill_table_gipedo()
                onomateponimo=combo3.get()
                if(not onomateponimo==''):
                
                    if(check_sinonimia()):
                        tilefono=combo4.get()
                    
                        if(not tilefono==''):
                            fill_table_proponiti()
                            fill_table_orario()
                    else:
                        fill_table_proponiti()
                        fill_table_orario()

        l1=tk.Label(w,text='DATE:')
        l1.place(x=20,y=10)
        imerominies=create_imerominies_epomenon_efta_imeron()
        combo1 = ttk.Combobox(w,state="readonly", values=imerominies)
        combo1.place(x=150,y=10)
        combo1.bind("<<ComboboxSelected>>", fill_tables)
        la=tk.Label(w,text='')
        lb=tk.Label(w,text='')
        lc=tk.Label(w,text='')


        def plirofories_gipedou(a):
            arithmos=combo2.get()
            eidos_gipedou,dieuthinsi,kostos_aneks_kratisis= Sql.find_plirofories_gipedou(self.conn,arithmos)
            s1="COURT TYPE: "+eidos_gipedou
            s2='ADDRESS: '+dieuthinsi
            s3='RESERV COST (NO TUTOR): '+str(kostos_aneks_kratisis)
            la.config(text=s1)
            lb.config(text=s2)
            lc.config(text=s3)

            la.place(x=300,y=30)
            lb.place(x=480,y=30)
            lc.place(x=710,y=30)

            date=combo1.get()
            if(date!=''):
                fill_table_gipedo()

        l2=tk.Label(w,text='COURT NUMBER:')
        l2.place(x=20,y=30)
        arithmos_gipedou=Sql.find_kodikous_gipedon(self.conn)
        combo2 = ttk.Combobox(w,state="readonly", values=arithmos_gipedou)
        combo2.place(x=150,y=30)
        combo2.bind("<<ComboboxSelected>>", plirofories_gipedou)

        def updtcblist():
            eponimo,onoma=combo3.get().split(' ')
            tilefona=Sql.find_tilefono_prosopikou(self.conn,onoma,eponimo)
            combo4['values'] = tilefona

        l5=tk.Label(text='')

        def find_plirofories_proponiti(a):
            eponimo,onoma=combo3.get().split(' ')
            tilefono=combo4.get()
            if(check_sinonimia()):

                
                if(not tilefono==''):
                    tilefono=int(tilefono)
                    kostos=str(Sql.find_kostos_idiaiterou(self.conn,onoma,eponimo,tilefono))
                    l5.config(text= 'PRIV LESSON COST:'+kostos)
                    l5.place(x=300,y=50)
            else:
                tilefono=int(Sql.find_tilefono_prosopikou(self.conn,onoma,eponimo)[0])
                kostos=str(Sql.find_kostos_idiaiterou(self.conn,onoma,eponimo,tilefono))
                l5.config(text= 'PRIV LESSON COST:'+kostos)
                l5.place(x=300,y=50)

            fill_tables(1)

        combo4 = ttk.Combobox(w,state="readonly", values=[],postcommand = updtcblist)
        combo4.bind("<<ComboboxSelected>>", find_plirofories_proponiti)

        l4=tk.Label(w,text='TUTOR PHONE')
        l5=tk.Label(w,text='PRIV LESSON COST:')

        def check_sinonimia():
            
            eponimo,onoma=combo3.get().split(' ')
            if(Elegxoi.check_sinonimia(self.conn,onoma,eponimo)):
                combo4.place(x=150,y=70)
                l4.place(x=20,y=70)
                return(True)
                
            else:
                combo4.place_forget()
                l4.place_forget()
                return False

        l3=tk.Label(w,text='TUTOR NAME:')
        l3.place(x=20,y=50)
        onomateponima_proponiton=Sql.find_onomateponima_proponiton(self.conn)
        combo3 = ttk.Combobox(w,state="readonly", values=onomateponima_proponiton)
        combo3.place(x=150,y=50)
        combo3.bind("<<ComboboxSelected>>", find_plirofories_proponiti)

        f0=tk.Frame(w,bg='green')
        f1=tk.Frame(w,bg='red')
        f2=tk.Frame(w,bg='blue')


        f0.config(width=400,height=550)
        f0.place(x=30,y=180)


        f1.config(width=400,height=550)
        f1.place(x=450,y=180)  

        f2.config(width=120,height=550)
        f2.place(x=870,y=180)    

        tree = ttk.Treeview(f0, columns=("size", "modified"))
        tree["columns"] = ("Occupied_hours")

        tree.column("Occupied_hours", width=20)
        

        tree.column('#0',width=0,stretch=0)
        tree.heading("Occupied_hours", text="Occupied hours of court")
        tree.place(width=450,height=550)


        tree2 = ttk.Treeview(f1, columns=("size", "modified"))
        tree2["columns"] = ("Occupied_hours_of_instructor")

        tree2.column("Occupied_hours_of_instructor", width=20)
        

        tree2.column('#0',width=0,stretch=0)
        tree2.heading("Occupied_hours_of_instructor", text="Occupied hours of instructor")
    
        tree2.place(width=450,height=550)

        tree3 = ttk.Treeview(f2, columns=("size", "modified"))
        tree3["columns"] = ("Tutor_schedule")

        tree3.column("Tutor_schedule", width=20)
        

        tree3.column('#0',width=0,stretch=0)
        tree3.heading("Tutor_schedule", text="Tutor schedule.")
        tree3.place(width=120,height=550)


        def fill_table_gipedo():
            
            tree.delete(*tree.get_children())
            arithmos=combo2.get()
            date=combo1.get()
            desmeumenes_ores_gipedou=Sql.find_ores_kai_imerominia_pou_einai_desmeumeno_to_gipedo_gia_mia_imerominia(self.conn,arithmos,date) 
            res=[] 
            for kataxorisi in desmeumenes_ores_gipedou:
                    res.append(kataxorisi[0])

            res.sort()

            for ora in res:
                    tree.insert("","end",values = (ora))

        def fill_table_proponiti():
            
            tree2.delete(*tree2.get_children())
            
            eponimo,onoma=combo3.get().split(' ')
            if(check_sinonimia()==False):
                tilefono=int(Sql.find_tilefono_prosopikou(self.conn,onoma,eponimo)[0])
            
            else:
                tilefono=int(combo4.get())
            kodikos=Sql.find_kodikos_proponiti(self.conn,onoma,eponimo,tilefono)
            imerominia=combo1.get()
            piasmenes_ores=Query.find_piasmenes_ores_proponiti_gia_imerominia(kodikos,imerominia)
            for ora in piasmenes_ores:
                    tree2.insert("","end",values = (ora))
        
        def fill_table_orario():

            tree3.delete(*tree3.get_children())

            eponimo,onoma=combo3.get().split(' ')
            if(check_sinonimia()==False):
                tilefono=int(Sql.find_tilefono_prosopikou(self.conn,onoma,eponimo)[0])
            
            else:
                tilefono=int(combo4.get())
            kodikos=Sql.find_kodikos_proponiti(self.conn,onoma,eponimo,tilefono)
            imerominia=combo1.get()
            mera=Utility.convert_dateObject_to_weekday(Utility.convert_date_to_dateObject(imerominia))
            orario=Query.find_orario_proponiti_gia_mia_mera(self.conn,kodikos,mera)
        

            for ora in orario:
                tree3.insert("","end",values = (ora))

        l10=tk.Label(w,text='MEMBER FIRST NAME:')
        l11=tk.Label(w,text='MEMBER LAST NAME:')
        l12=tk.Label(w,text='PHONE NUMBER:')

        l10.place(x=340,y=110)
        l11.place(x=340,y=85)
       

        e1=tk.Entry(w,width=15)
        e2=tk.Entry(w,width=15)
        
        
        e1.place(x=460,y=110)
        e2.place(x=460,y=85)

        def elegxos_sinonimias():
            onoma_melous=self.format_string(e1.get())
            eponimo_melous=self.format_string(e2.get())
            tilefona_melous=Sql.find_tilefona_melous(self.conn,onoma_melous,eponimo_melous)
            if(len(tilefona_melous)>1):
                combo_tilefono.place(x=510,y=140)
                l12.place(x=380,y=140)
                combo_tilefono["values"]=tilefona_melous
            else:
                combo_tilefono.place_forget()
                l12.place_forget()



        b10=tk.Button(w,text='Same name check',command=elegxos_sinonimias)
        b10.place(x=560,y=105)


        combo_tilefono = ttk.Combobox(w,state="readonly", values=[])

        def show_time(a):
            ora=combo_ora.get()
            lepta=combo_lepta.get()
            if(ora!='' and lepta!=''):
                ora_int_enarksis=int(ora)
                lepta_int_enarksis=int(lepta)
                diarkia=Utility.convert_ora(ora_int_enarksis,lepta_int_enarksis)
                l15.configure(text=diarkia)

        ores_values=['08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
        combo_ora= ttk.Combobox(w,state="readonly", values=ores_values,width=2)
        combo_ora.place(x=750,y=80)
        combo_ora.bind("<<ComboboxSelected>>", show_time)


        lepta_values=['00','05','10','15','20','25','30','35','40','45','50','55']
        combo_lepta= ttk.Combobox(w,state="readonly", values=lepta_values,width=2)
        combo_lepta.place(x=750,y=110)
        combo_lepta.bind("<<ComboboxSelected>>", show_time)


        l13=tk.Label(w,text='HOUR')
        l14=tk.Label(w,text='MIN')
        l15=tk.Label(w,text='')
        l16=tk.Label(w,text='TIME')

        l13.place(x=700,y=80)
        l14.place(x=700,y=110)
        l15.place(x=700,y=140)
        l16.place(x=640,y=140)


        def dimiourgia_kratisis(button):
            imerominia=combo1.get()
            ora=l15.cget("text")
            gipedo=combo2.get()
            onoma_melous=self.format_string(e1.get())
            eponimo_melous=self.format_string(e2.get())
            tilefono_melous=''
            tilefono_proponiti=''
            

            if(onoma_melous!='' and eponimo_melous!=''):
                tilefona_melous=Sql.find_tilefona_melous(self.conn,onoma_melous,eponimo_melous)
                if(len(tilefona_melous)==0):
                    tk.messagebox.showerror("Not found", "Member not found",parent=w)
                    return
                elif(len(tilefona_melous)>1):
                    try:
                        tilefono_melous=int(combo_tilefono.get())
                    except:
                        pass
                else:
                    tilefono_melous=int(tilefona_melous[0])

            onomateponimo_proponiti=combo3.get()

            if(onomateponimo_proponiti!=''):
                eponimo_proponiti,onoma_proponiti=onomateponimo_proponiti.split(' ')
                tilefona_proponiti=Sql.find_tilefono_prosopikou(self.conn,onoma_proponiti,eponimo_proponiti)

                if(len(tilefona_proponiti)>1):
                    try:
                        tilefono_proponiti=int(combo4.get())
                    except:
                        pass
                else:
                    tilefono_proponiti=int(tilefona_proponiti[0])
            if(button=="With instructor"):
                if(onomateponimo_proponiti!='' and imerominia!='' and ora!='' and gipedo!='' and onoma_melous!='' and eponimo_melous!='' and tilefono_proponiti!='' and tilefono_melous!=''):
                    kodikos_melous=Sql.find_kodikos_melous(self.conn,onoma_melous,eponimo_melous,tilefono_melous)
                    kodikos_proponiti=Sql.find_kodikos_proponiti(self.conn,onoma_proponiti,eponimo_proponiti,tilefono_proponiti)
                    if(not Utility.dimiourgia_ksexoristis_kratisis(self.conn,imerominia,ora,gipedo,kodikos_melous,kodikos_proponiti)):
                        tk.messagebox.showerror("Overlap", "Hour is not available",parent=w)
                    else:
                        fill_tables(1)
                else:
                    tk.messagebox.showerror("Missing values", "Missing information",parent=w)
     
            elif(button=="Without instructor"):
                if( imerominia!='' and ora!='' and gipedo!='' and onoma_melous!='' and eponimo_melous!='' and tilefono_melous!=''):
                    kodikos_melous=Sql.find_kodikos_melous(self.conn,onoma_melous,eponimo_melous,tilefono_melous)
                    kodikos_proponiti=None
                    if(not Utility.dimiourgia_ksexoristis_kratisis(self.conn,imerominia,ora,gipedo,kodikos_melous,kodikos_proponiti)):
                        tk.messagebox.showerror("Overlap", "There is time overlap",parent=w)
                    else:
                        fill_tables(1)

                else:
                    tk.messagebox.showerror("Missing values", "Missing information",parent=w)
     



        b20=tk.Button(w,text='Without instructor',command= lambda t= "Without instructor": dimiourgia_kratisis(t),height=2)
        b20.place(x=810,y=75)

        b21=tk.Button(w,text='With instructor',command= lambda t= "With instructor": dimiourgia_kratisis(t),height=2)
        b21.place(x=810,y=120)

    def create_menu_eggrafis_melon(self):
        
        w2 = tk.Toplevel(self.frame0)
        w2.geometry('400x400')
        w2.resizable(False, False)
        l1=tk.Label(w2,text='FIRST NAME:')
        l1.place(x=20,y=20,height=30)
        e1=tk.Entry(w2)
        e1.place(x=120,y=20,height=30)
        
        l2=tk.Label(w2,text='LAST NAME:')
        l2.place(x=20,y=60,height=30)
        e2=tk.Entry(w2)
        e2.place(x=120,y=60,height=30)

        l3=tk.Label(w2,text='PHONE:')
        l3.place(x=20,y=100,height=30)
        e3=tk.Entry(w2)
        e3.place(x=120,y=100,height=30)

        l4=tk.Label(w2,text='YEAR RANGE:')
        l4.place(x=20,y=150,height=30)
        ilikies=['UNDER 10','10-12','13-15','16-17','ADULT']
        combo = ttk.Combobox(w2,state="readonly", values=ilikies)
        combo.place(x=120,y=150)

        l5=tk.Label(w2,text='SEX')
        l5.place(x=20,y=190,height=30)
        filo=['W','M']
        combo2 = ttk.Combobox(w2,state="readonly", values=filo)
        combo2.place(x=120,y=190)
        

        def eggrafi_melous():
            onoma=self.format_string(e1.get())
            eponimo=self.format_string(e2.get())
            tilefono=self.format_tilefono(e3.get())

            if(len(tilefono)!=10):
                tk.messagebox.showerror("Wrong number", "Missing digits in phone number",parent=w2)
                return
                
            ilikiako_euros=combo.get()
            filo=combo2.get()
            if(onoma!='' and eponimo!='' and tilefono!='' and ilikiako_euros!='' and filo!='' ):
                if(not Elegxoi.melosExists(onoma,eponimo,tilefono)):
                    if(not tilefono.isdigit()):
                        tk.messagebox.showerror("Invalid phone number", "Phone number can't contain letters",parent=w2)
                    elif(not onoma.isalpha() or not eponimo.isalpha()):
                        tk.messagebox.showerror("Invalid name", "Name must contain only letters",parent=w2)
                    else:
                        imerominia=Utility.find_current_date()
                        tilefono=int(tilefono)
                        Sql.add_melos(self.conn,onoma,eponimo,imerominia,tilefono,filo,ilikiako_euros)
                        l4=tk.Label(w2,text="SUCCESSFUL SIGNUP")
                        l4.place(x=180,y=350,height=30)

                else:
                    tk.messagebox.showerror("Already exists", "Member already exists",parent=w2)
            else:
                tk.messagebox.showerror("Missing fields", "Missing information",parent=w2)
            

        b=tk.Button(w2,text='SIGN UP',command=eggrafi_melous)
        b.place(x=300,y=330,height=50)
    
    def create_menu_mathimaton_proponiton(self):
        w = tk.Toplevel(self.frame0)
        w.geometry('1000x800')
        w.resizable(False, False)


        l1=tk.Label(w,text='TUTOR NAME:')
        l1.place(x=20,y=20)
        onomat_proponiton=Sql.find_onomateponima_proponiton(self.conn)
        onomateponima_proponiton=[]
        
        for kataxorisi in onomat_proponiton:
            onomateponima_proponiton.append((kataxorisi[0],kataxorisi[1]))
        onomateponima_proponiton.sort()


        l2=tk.Label(w,text='FUTURE COURSES FOR PRIVATE LESSON ')
        l3=tk.Label(w,text='GROUPS')
        l2.place(x=560,y=140)
        l3.place(x=200,y=140)


        def updtcblist():
            eponimo,onoma=combo1.get().split(' ')
            tilefona=Sql.find_tilefono_prosopikou(self.conn,onoma,eponimo)
            combo2['values'] = tilefona
        

        l2=tk.Label(w,text='INST PHONE')

        def check_sinonimia():
            
            eponimo,onoma=combo1.get().split(' ')
            if(Elegxoi.check_sinonimia(self.conn,onoma,eponimo)):
                combo2.place(x=150,y=50)
                l2.place(x=20,y=50)
                return(True)
                
            else:
                combo2.place_forget()
                l2.place_forget()
                return False

        def fill_tables(a):
            eponimo,onoma=combo1.get().split(' ')
            if(check_sinonimia()):
               tilefono=combo2.get()
               if(tilefono==''):return

            else:
                tilefono=int(Sql.find_tilefono_prosopikou(self.conn,onoma,eponimo)[0])

                

            kodikos_proponiti=Sql.find_kodikos_proponiti(self.conn,onoma,eponimo,tilefono)

            aneksartites_kratisis=Sql.find_melontikes_aneksartites_kratisis_proponiti(self.conn,kodikos_proponiti)
            anaplirosis=Sql.find_melontikes_anaplirosis_proponiti(self.conn,kodikos_proponiti)
            kratisis=aneksartites_kratisis+anaplirosis
            didaskalies=Sql.find_didaskalies_proponiti(self.conn,kodikos_proponiti,Utility.find_current_year_period())

            sorted_kratisis_by_imerominia= sorted(kratisis, key=lambda tup: tup[1])

            tree.delete(*tree.get_children())
            tree2.delete(*tree2.get_children())

            for kataxorisi in sorted_kratisis_by_imerominia:
                kodikos,imerominia,ora,gipedo,dieuthinsi=kataxorisi
                tree2.insert("","end",values = (imerominia,ora,gipedo,dieuthinsi))

            for kataxorisi in didaskalies:
                ora,mera,epipedo,etos,noumero=kataxorisi
                tree.insert("","end",values = (ora,mera,epipedo,etos,noumero))


        combo1 = ttk.Combobox(w,state="readonly", values=onomateponima_proponiton)
        combo1.place(x=150,y=20)
        combo1.bind("<<ComboboxSelected>>", fill_tables)


        combo2 = ttk.Combobox(w,state="readonly", values=[],postcommand = updtcblist)
        combo2.bind("<<ComboboxSelected>>", fill_tables)

        
        f1=tk.Frame(w)
        f2=tk.Frame(w)


        f1.config(width=450,height=750)
        f1.place(x=30,y=180)  

        f2.config(width=450,height=750)
        f2.place(x=500,y=180)    

        tree = ttk.Treeview(f1, columns=("size", "modified"))
        tree["columns"] = ("HOUR","DAY","LEVEL",'YEAR','NUMBER')

        tree["columns"] = ("HOUR", "DAY", "LEVEL","YEAR", 'NUMBER')

        tree.column("HOUR", width=30)
        tree.column("DAY", width=30)
        tree.column("LEVEL", width=30)
        tree.column("YEAR", width=30)
        tree.column("NUMBER", width=30)

        tree.column('#0',width=0,stretch=0)
        tree.heading("HOUR", text="HOUR")
        tree.heading("DAY", text="DAY")
        tree.heading("LEVEL", text="LEVEL")
        tree.heading("YEAR", text="YEAR")
        tree.heading("NUMBER", text="NUMBER")

        tree.place(width=450,height=750)

        tree2 = ttk.Treeview(f2, columns=("size", "modified"))
        tree2["columns"] = ("DATE","HOUR","COURT_NUMBER",'ADDRESS')

        tree2["columns"] = ("DATE", "HOUR", "COURT_NUMBER","ADDRESS")

        tree2.column("DATE", width=30)
        tree2.column("HOUR", width=30)
        tree2.column("COURT_NUMBER", width=30)
        tree2.column("ADDRESS", width=30)
        
        tree2.column('#0',width=0,stretch=0)
        tree2.heading("DATE", text="DATE")
        tree2.heading("HOUR", text="HOUR")
        tree2.heading("COURT_NUMBER", text="COURT NUMBER")
        tree2.heading("ADDRESS", text="ADDRESS")

        tree2.place(width=450,height=750)
    
    def create_menu_kratisis_didaskalion(self):
        w = tk.Toplevel(self.frame0)
        w.geometry('1000x800')
        w.resizable(False, False)

        l1=tk.Label(w,text='COURSE:')
        l1.place(x=20,y=10)
        didaskalies=Sql.find_didaskalies(self.conn,Utility.find_current_year_period())
        epipedo_kai_noumero=[]
        for kataxorisi in didaskalies:
            epipedo_kai_noumero.append((kataxorisi[0],kataxorisi[2]))
        epipedo_kai_noumero.sort()

        def fill_table(a):
            epipedo,noumero=combo1.get().split(' ')
            etos=Utility.find_current_year_period()
            kratisis=Sql.find__melontikes_kratisis_mias_didaskalias(self.conn,epipedo,etos,noumero)

            tree.delete(*tree.get_children())

            for kataxorisi in kratisis:
                tree.insert("","end",values = kataxorisi)

        
        combo1 = ttk.Combobox(w,state="readonly", values=epipedo_kai_noumero)
        combo1.place(x=150,y=10)
        combo1.bind("<<ComboboxSelected>>", fill_table)

        f1=tk.Frame(w)
        f1.config(width=620,height=650)
        f1.place(x=30,y=120)    

        tree = ttk.Treeview(f1, columns=("size", "modified"))
        tree["columns"] = ("date","hour",'court_number','address')

        tree.column("date", width=20)
        tree.column("hour", width=20)
        tree.column("court_number", width=20)
        tree.column("address", width=20)
        

        tree.column('#0',width=0,stretch=0)
        tree.heading("date", text="date")
        tree.heading("hour", text="hour")
        tree.heading("court_number", text="court number")
        tree.heading("address", text="address")
        tree.place(width=620,height=550)



Gui()



# runs the simulation to fill database for the year 2023-2024

# print('start')
# Simulate()
# print('end')



