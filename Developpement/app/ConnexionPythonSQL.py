from dataclasses import dataclass
from email.headerregistry import DateHeader
from logging import exception
from sqlite3 import DatabaseError
from statistics import quantiles
from wsgiref.validate import PartialIteratorWrapper
import sqlalchemy
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy import Column , Integer, Text , Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from .Exposant import Exposant
from .Consommateur import Consommateur
from .Staff import Staff
from .Intervenant import Intervenant
from .Auteur import Auteur
from .Presse import Presse
from .Invite import Invite
from .Participant import Participant
from .Loger import Loger
from .Hotel import Hotel
from .Manger import Manger
from .Repas import Repas
from .Creneau import Creneau
from .Restaurant import Restaurant

# pour avoir sqlalchemy :
# sudo apt-get update 
# sudo apt-get install python3-sqlalchemy
# pip3 install mysql-connector-python
ROLE = ["Auteur", "Exposant", "Staff", "Presse", "Invite"]

def ouvrir_connexion(user,passwd,host,database):
    """
    ouverture d'une connexion MySQL
    paramètres:
       user     (str) le login MySQL de l'utilsateur
       passwd   (str) le mot de passe MySQL de l'utilisateur
       host     (str) le nom ou l'adresse IP de la machine hébergeant le serveur MySQL
       database (str) le nom de la base de données à utiliser
    résultat: l'objet qui gère le connection MySQL si tout s'est bien passé
    """
    try:
        #creation de l'objet gérant les interactions avec le serveur de BD
        engine=sqlalchemy.create_engine('mysql+mysqlconnector://'+user+':'+passwd+'@'+host+'/'+database)
        #creation de la connexion
        cnx = engine.connect()
    except Exception as err:
        print(err)
        raise err
    print("connexion réussie")
    return cnx,engine

#connexion ,engine = ouvrir_connexion("charpentier","charpentier",'servinfo-mariadb', "DBcharpentier")
connexion ,engine = ouvrir_connexion("nardi","nardi","servinfo-mariadb", "DBnardi")
# if __name__ == "__main__":
#     login=input("login MySQL ")
#     passwd=getpass.getpass("mot de passe MySQL ")
#     serveur=input("serveur MySQL ")
#     bd=input("nom de la base de données ")
#     cnx=ouvrir_connexion(login,passwd,serveur,bd)
#     # ici l'appel des procédures et fonctions
#     cnx.close()
Session = sessionmaker(bind=engine)
session = Session()

def get_max_id_participant(session):
    max_id = session.query(func.max(Participant.idP)).first()
    
    if (max_id[0]) is None:
        return 0
    else:
        return max_id[0]

def get_max_num_stand(session):
    max_num = session.query(func.max(Exposant.numStand)).first()
    if (max_num[0]) is None:
        return 0
    else:
        return max_num._data[0]

def ajoute_particpant(session, participant):
    personneP = session.query(Participant).filter(Participant.idP == participant.idP).first()
    if personneP is None:
        participant.idP = get_max_id_participant(session) + 1
        session.add(participant)
        try:
            session.commit()
            print("La Participant "+ str(participant) +" a bien été inséré dans la base de donnée")
        except:
            print("Erreur")
    else:
        print("Une personne a déjà cet identifiant dans la base de donnée")
        
def ajoute_participant_id(session, participant):
    personneP = session.query(Participant).filter(Participant.idP == participant.idP).first()
    if personneP is None:
        participant.idP = participant.idP
        session.add(participant)
        try:
            session.commit()
            print("La Participant "+ str(participant) +" a bien été inséré dans la base de donnée")
        except:
            print("Erreur")
    else:
        print("Une personne a déjà cet identifiant dans la base de donnée")
    
def ajoute_Consommateur(session, consommateur):
    consommateurC = session.query(Consommateur).filter(Consommateur.idP == consommateur.idP).first()
    if consommateurC is None:
        personne = session.query(Participant).filter(Participant.idP == consommateur.idP).first()
        new_consommateur = Consommateur(consommateur.idP)
        session.add(new_consommateur)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu un(e) consommateur")
        except:
            print("Erreur")
            session.rollback()
    else:
        print("Un consommateur a déjà cet identifiant dans la base de donnée")

def ajoute_exposant(session, exposant):
    exposantE = session.query(Exposant).filter(Exposant.idP == exposant.idP).first()
    if exposantE is None:
        personne = session.query(Participant).filter(Participant.idP == exposant.idP).first()
        new_exposant = Exposant(exposant.idP, get_max_num_stand(session) + 1)
        session.add(new_exposant)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu un(e) exposant(e)")
        except:
            print("Erreur")
            session.rollback()
    else:
        print("Un exposant a déjà cet identifiant dans la base de donnée")

def ajoute_staff(session, staff):
    staffS = session.query(Staff).filter(Staff.idP == staff.idP).first()
    if staffS is None:
        personne = session.query(Participant).filter(Participant.idP == staff.idP).first()
        new_staff = Staff(staff.idP)
        session.add(new_staff)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu un(e) staff")
        except:
            print("Erreur")
            session.rollback()
    else:
        print("Un staff a déjà cet identifiant dans la base de donnée")
        
def ajoute_intervenant(session, intervenant):
    intervenantI = session.query(Intervenant).filter(Intervenant.idP == intervenant.idP).first()
    if intervenantI is None:
        personne = session.query(Participant).filter(Participant.idP == intervenant.idP).first()
        new_intervenant = Intervenant(intervenant.idP, None, None)
        session.add(new_intervenant)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu un(e) intervenant(e)")
        except:
            print("Erreur")
            session.rollback()
    else:
        print("Un intervenant a déjà cet identifiant dans la base de donnée")
    
def ajoute_auteur(session, auteur):
    auteurA = session.query(Auteur).filter(Auteur.idP == auteur.idP).first()
    if auteurA is None:
        personne = session.query(Participant).filter(Participant.idP == auteur.idP).first()
        new_auteur = Auteur(auteur.idP, None)
        session.add(new_auteur)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu un(e) auteur / autrice")
        except:
            print("Erreur")
            session.rollback()
    else:
        print("Un auteur a déjà cet identifiant dans la base de donnée")

def ajoute_presse(session, presse):
    presseP = session.query(Presse).filter(Presse.idP == presse.idP).first()
    if presseP is None:
        personne = session.query(Participant).filter(Participant.idP == presse.idP).first()
        new_presse = Presse(presse.idP)
        session.add(new_presse)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu membre de la presse")
        except:
            print("Erreur")
            session.rollback()
    else:
        print("Une personne de la presse a déjà cet identifiant dans la base de donnée")

def ajoute_invite(session, invite):
    inviteI = session.query(Invite).filter(Invite.idP == invite.idP).first()
    if inviteI is None:
        personne = session.query(Participant).filter(Participant.idP == invite.idP).first()
        new_invite = Invite(invite.idP)
        session.add(new_invite)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu un(e) invité(e)")
        except:
            print("Erreur")
            session.rollback()
    else:
        print("Un invité a déjà cet identifiant dans la base de donnée")
        

        
def ajoute_participant_role(session, participant, role):
    if role in ROLE:
        ajoute_particpant(session, participant)
        if role == "Exposant":
            ajoute_exposant(session, participant)
        else:
            ajoute_Consommateur(session, participant)
            if role == "Staff":
                ajoute_staff(session, participant)
            else:
                ajoute_intervenant(session, participant)
                if role == "Auteur":
                    ajoute_auteur(session, participant)
                elif role == "Presse":
                    ajoute_presse(session, participant)
                else:
                    ajoute_invite(session, participant)
    else:
        print("Le rôle n'est pas reconnu")

def ajoute_participant_role_id(session, participant, role):
    if role in ROLE:
        ajoute_participant_id(session, participant)
        if role == "Exposant":
            ajoute_exposant(session, participant)
        else:
            ajoute_Consommateur(session, participant)
            if role == "Staff":
                ajoute_staff(session, participant)
            else:
                ajoute_intervenant(session, participant)
                if role == "Auteur":
                    ajoute_auteur(session, participant)
                elif role == "Presse":
                    ajoute_presse(session, participant)
                else:
                    ajoute_invite(session, participant)
    else:
        print("Le rôle n'est pas reconnu")    
        
def supprimer_participant(session, id_participant):
    session.query(Participant).filter(Participant.idP == id_participant).delete()
    session.commit()
    print("Le participant a été supprimé")

def supprimer_consommateur(session, id_consommateur):
    session.query(Consommateur).filter(Consommateur.idP == id_consommateur).delete()
    session.commit()
    print("Le consommateur a été supprimé")

def supprimer_intervenant(session, id_intervenant):
    session.query(Intervenant).filter(Intervenant.idP == id_intervenant).delete()
    session.commit()
    print("L'intervenant a été supprimé")

def supprimer_exposant(session, id_exposant):
    session.query(Exposant).filter(Exposant.idP == id_exposant).delete()
    session.commit()
    print("L'exposant a été supprimé")
  
def supprimer_staff(session, id_staff):
    session.query(Staff).filter(Staff.idP == id_staff).delete()
    session.commit()
    print("Le staff a été supprimé")

def supprimer_auteur(session, id_auteur):
    session.query(Auteur).filter(Auteur.idP == id_auteur).delete()
    session.commit()
    print("L'auteur a été supprimé")

def supprimer_presse(session, id_presse):
    session.query(Presse).filter(Presse.idP == id_presse).delete()
    session.commit()
    print("Le membre de la presse a été supprimé")

def supprimer_invite(session, id_invite):
    session.query(Invite).filter(Invite.idP == id_invite).delete()
    session.commit()        
    print("L'invité a été supprimé")
     
def supprimer_participant_role(session, id_participant):
    participant_existe = session.query(Participant).filter(Participant.idP == id_participant).first()
    if participant_existe is not None:
        exposant = session.query(Exposant).filter(Exposant.idP == id_participant).first()
        staff = session.query(Staff).filter(Staff.idP == id_participant).first()
        auteur = session.query(Auteur).filter(Auteur.idP == id_participant).first()
        presse = session.query(Presse).filter(Presse.idP == id_participant).first()
        invite = session.query(Invite).filter(Invite.idP == id_participant).first()
        if exposant is not None:
            supprimer_exposant(session, id_participant)
        else:
            if staff is not None:
                supprimer_staff(session, id_participant)
            else:
                if auteur is not None:
                    supprimer_auteur(session, id_participant)
                elif presse is not None:
                    supprimer_presse(session, id_participant)
                elif invite is not None:
                    supprimer_invite(session, id_participant)
                supprimer_intervenant(session, id_participant)
            supprimer_consommateur(session, id_participant)
        supprimer_participant(session, id_participant)
    else:
        print("La personne que vous voulez supprimer n'existe pas")

     
def modifier_participant(session, participant):
    session.query(Participant).filter(Participant.idP == participant.idP).update(
        {Participant.prenomP : participant.prenomP, Participant.nomP : participant.nomP, Participant.ddnP : participant.ddnP, 
         Participant.telP : participant.telP, Participant.emailP : participant.emailP, Participant.mdpP : participant.mdpP,
         Participant.invite : participant.invite, Participant.emailEnvoye : participant.emailEnvoye, Participant.remarques : participant.remarques})
    session.commit()
    print("Le participant a bien été modifié")        

def modifier_participant_role(session, participant, metier):
    ancien_participant = Participant(participant.idP, participant.prenomP, participant.nomP, participant.ddnP, participant.telP, participant.emailP, participant.mdpP, participant.remarques, participant.invite, participant.emailEnvoye)
    supprimer_participant_role(session, participant.idP)
    ajoute_participant_role_id(session, ancien_participant, metier)
    print("Le role du participant a bien été modifié")

def modif_loger(session, ancien_loger, nouveau_loger):
    session.query(Loger).filter(Loger.idP == ancien_loger.idP).filter(Loger.idHotel == ancien_loger.idHotel).filter(Loger.dateDeb == ancien_loger.dateDeb).update({
        Loger.idHotel : nouveau_loger.idHotel, Loger.dateDeb : nouveau_loger.dateDeb, Loger.dateFin : nouveau_loger.dateFin})
    session.commit()
    print("Le logement de cette personne a bien été modifié")        

def modif_repas(session, ancien_repas, nouveau_repas):
    session.query(Manger).filter(Manger.idP == ancien_repas.idP).filter(Manger.idRepas == ancien_repas.idRepas).update(
        {Manger.idRepas : nouveau_repas.idRepas}
    )
    session.commit()
    print("Le repas du participant a bien été modifié")     

def get_info_personne(session, email, mdp):
    personne = session.query(Participant).filter(Participant.emailP == email).filter(Participant.mdpP == mdp).first()
    if personne is None:
        return False
    else:
        return (True, personne)

def get_participant(session, id_participant):
    return session.query(Participant).filter(Participant.idP == id_participant).first()

def get_id_hotel(session, nom_hotel):
    return (session.query(Hotel).filter(Hotel.nomHotel == nom_hotel).first()).idHotel
   
def affiche_participants(session):
    liste_participants = []
    participants = session.query(Participant)
    for part in participants:
        liste_participants.append(part)
    return liste_participants
   
#print(affiche_participants(session))
   
def affiche_participant_date(session, date, restaurant, midi):
    liste_consommateurs = []
    creneau = session.query(Creneau).filter(Creneau.dateDebut[:10] == date)
    restaurant = session.query(Restaurant).filter(Restaurant.nomRest == restaurant).first()
    repas, consommateurs = None, None
    
    for line in creneau:
        repas += session.query(Repas).filter(Repas.idRest == restaurant.idRest).filter(Repas.estMidi == midi).filter(Repas.idCreneau == line.idCreneau)
    for ligne in repas:
        consommateurs += session.query(Manger).filter(Manger.idRepas == ligne.idRepas)
    
    for consomm in consommateurs:
        liste_consommateurs.append(consomm)
    return liste_consommateurs
   
   
# def affiche_participant_date2(session, date, restaurant, midi):
#     liste_consommateurs = []
#     liste_creneau = []
#     creneau = session.query(Creneau.dateDebut).all()
#     for cren in creneau:
#         if cren[0].date() == date:
#             liste_creneau.append(cren)
        
#     print(liste_creneau[0])
#     creneau2 = session.query(Creneau).filter(Creneau.dateDebut == liste_creneau[0]).all()
#     print(creneau2)
#     restaurant = session.query(Restaurant).filter(Restaurant.nomRest == restaurant).first()
    
#     repas = session.query(Repas, creneau).filter(Repas.idRest == restaurant.idRest).filter(Repas.estMidi == midi).join(Creneau).filter(Repas.idCreneau == creneau.idCreneau).all()
#     consommateurs = session.query(Manger, repas).filter(Manger.idRepas == repas.idRepas)

#     for consomm in consommateurs:
#         liste_consommateurs.append(consomm)
#     return liste_consommateurs

# print(affiche_participant_date2(session, datetime.datetime(2022,11,18,11,30).date(), "Erat Eget Tincidunt Incorporated", True))
                
# ajoute_personne(session, Participant(None, "a", "a", "2003-08-18", "0607080911", "maxym.charpentier@gmail.com", "A", False, False,"aucune", "Voiture"))
# ajoute_Consommateur(session, Consommateur(1))
# ajoute_exposant(session, Exposant(1, 1))
# ajoute_staff(session, Staff(1))
# ajoute_intervenant(session, Intervenant(1, "2020-03-03 12:00:00", "2020-03-03 13:00:00", "voiture", "aucune"))
# ajoute_auteur(session, Auteur(1, 1))
# ajoute_presse(session, Presse(1))
# ajoute_invite(session, Invite(1))
#ajoute_participant_role(session, Participant(None, "Mathieu", "Alpha", "2003-08-18", "0606060666", "maxym.charpentier@gmail.com", "A", "aucune", emailEnvoye = True), "Auteur")

#print(get_info_personne(session, "lenny@gmail.com", "le"))

#print(datetime.datetime.now().date())

#print(get_participant(session, 14))

#print(datetime.datetime(2022,11,18))

# ajoute_participant_role_id(session, Participant(14, "Mathieu", "Alpha", "2003-08-18", "0606060666", "maxym.charpentier@gmail.com", "A", "aucune", emailEnvoye = True), "Auteur")
# modifier_participant_role(session, get_participant(session, 14), "Exposant")
    
    
#ajoute_participant_role(session, Participant(None, "TEST PRENOM", "TEST NOM", "2003-08-18", "0606060666", "maxym.charpentier@gmail.com", "A", "aucune"), "Staff")
# supprimer_participant_role(session, 8)
#modifier_participant(session, Participant(7, "test", "test", "2005-08-18", "0700000000", "a.a@gmail.com", "b", "jsp", invite=True, emailEnvoye=True))