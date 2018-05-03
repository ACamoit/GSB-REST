#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import *
import json
import mysql.connector

app = Flask( __name__ )	

connexionBD = mysql.connector.connect(
			host = 'localhost' ,
			user = 'root' ,
			password = 'azerty' ,
			database = 'Gsb'
		)

if __name__ == '__main__':
	app.run( debug = True , host = '192.168.42.28' , port = 5000 )

########################    RETOURNE LES RAPPORTS DE VISITE ###########################

@app.route( '/rapports' , methods=['GET'] )
def getRapports() :
	curseur = connexionBD.cursor()
	curseur.execute( 'SELECT r.RAP_NUM, v.VIS_NOM, p.PRA_NOM, CONVERT(r.RAP_DATE, CHAR), r.RAP_BILAN, m.MOT_LIBELLE, v.VIS_VILLE, e.EVA_LIBELLE, r.ESTVU  From VISITEUR v INNER JOIN RAPPORT_VISITE r ON v.VIS_MATRICULE = r.VIS_MATRICULE INNER JOIN PRATICIEN p ON r.PRA_NUM = p.PRA_NUM INNER JOIN MOTIF m ON r.MOT_NUM = m.MOT_NUM INNER JOIN EVALUATION e ON r.EVA_NUM = e.EVA_NUM' )
	tuples = curseur.fetchall()
	curseur.close()
	rapports = []
	for unTuple in tuples :
		unRapport = { 'numRapport': unTuple[0] , 'nomVisiteur': unTuple[1] ,  'nomPraticien': unTuple[2] , 'rapDate': unTuple[3] , 'rapBilan': unTuple[4] , 'rapMotif': unTuple[5] , 'rapVille': unTuple[6] , 'rapEval': unTuple[7] , 'estVu': unTuple[8] }
		rapports.append( unRapport )
	reponse = json.dumps( rapports )
	print "Rapports : " + reponse
	return Response( reponse , status=200 , mimetype='application/json' ) 

########################    RETOURNE LE RAPPORT DE VISITE CORRESPONDANT AU NUMERO ENTRER EN PARAMETRE ###########################

@app.route( '/rapports/<rapNum>' , methods=['GET'] )
def getRapportsParNum( rapNum ) :
	pass

	curseur = connexionBD.cursor()
	curseur.execute( 'SELECT r.RAP_NUM, v.VIS_NOM, p.PRA_NOM, CONVERT(r.RAP_DATE, CHAR), r.RAP_BILAN, m.MOT_LIBELLE, v.VIS_VILLE, e.EVA_LIBELLE, r.ESTVU  From VISITEUR v INNER JOIN RAPPORT_VISITE r ON v.VIS_MATRICULE = r.VIS_MATRICULE INNER JOIN PRATICIEN p ON r.PRA_NUM = p.PRA_NUM INNER JOIN MOTIF m ON r.MOT_NUM = m.MOT_NUM INNER JOIN EVALUATION e ON r.EVA_NUM = e.EVA_NUM WHERE r.RAP_NUM = %s' , ( rapNum, ) )
	tuples = curseur.fetchall()
	curseur.close()
	rapports = []
	for unTuple in tuples :
		unRapport = { 'numRapport': unTuple[0] , 'nomVisiteur': unTuple[1] ,  'nomPraticien': unTuple[2] , 'rapDate': unTuple[3] , 'rapBilan': unTuple[4] , 'rapMotif': unTuple[5] , 'rapVille': unTuple[6] , 'rapEval': unTuple[7] , 'estVu': unTuple[8] }
		rapports.append( unRapport )
	reponse = json.dumps( rapports )
	print "Rapports : " + reponse
	return Response( reponse , status=200 , mimetype='application/json' ) 


########################    RETOURNE LES RAPPORTS DE VISITE CORRESPONDANT AU NOM_VISITEUR, MOIS ET ANNEE EN PARAMETRE ###########################

@app.route( '/rapports/<matricule>.<mois>.<annee>' , methods=['GET'] )
def getRapportsParVisMoisAnnee( matricule, mois, annee ) :
	pass

	curseur = connexionBD.cursor()
	curseur.execute( 'SELECT r.RAP_NUM, v.VIS_NOM, p.PRA_NOM, CONVERT(r.RAP_DATE, CHAR), r.RAP_BILAN, m.MOT_LIBELLE, v.VIS_VILLE, e.EVA_LIBELLE, r.ESTVU  From VISITEUR v INNER JOIN RAPPORT_VISITE r ON v.VIS_MATRICULE = r.VIS_MATRICULE INNER JOIN PRATICIEN p ON r.PRA_NUM = p.PRA_NUM INNER JOIN MOTIF m ON r.MOT_NUM = m.MOT_NUM INNER JOIN EVALUATION e ON r.EVA_NUM = e.EVA_NUM WHERE v.VIS_MATRICULE = %s AND MONTH(r.RAP_DATE) = %s AND YEAR(r.RAP_DATE) = %s ' , ( matricule, mois, annee ) )
	tuples = curseur.fetchall()
	curseur.close()
	rapports = []
	for unTuple in tuples :
		unRapport = { 'numRapport': unTuple[0] , 'nomVisiteur': unTuple[1] ,  'nomPraticien': unTuple[2] , 'rapDate': unTuple[3] , 'rapBilan': unTuple[4] , 'rapMotif': unTuple[5] , 'rapVille': unTuple[6] , 'rapEval': unTuple[7] , 'estVu': unTuple[8] }
		rapports.append( unRapport )
	reponse = json.dumps( rapports )
	print "Rapports : " + reponse
	return Response( reponse , status=200 , mimetype='application/json' )

########################    RETOURNE LE VISITEUR CORRESPONDANT AU MATRICULE ET AU MDP EN PARAMETRE ###########################

@app.route( '/connexion/<usr>.<pwd>' , methods=['GET'] )
def connexionUser( usr, pwd ) :
	pass

	curseur = connexionBD.cursor()
	curseur.execute( 'SELECT VIS_MATRICULE, VIS_NOM, VIS_PRENOM, VIS_ADRESSE, VIS_CP, VIS_VILLE, CONVERT(VIS_DATEEMBAUCHE, CHAR), VIS_MDP FROM VISITEUR WHERE VIS_MATRICULE = %s AND VIS_MDP = %s', ( usr, pwd ) )
	tuples = curseur.fetchall()
	curseur.close()
	for unTuple in tuples :
		uneConnexion = { 'mdp': unTuple[7] , 'dateembauche': unTuple[6] , 'ville': unTuple[5] , 'cp': unTuple[4] , 'adresse': unTuple[3] , 'prenom': unTuple[2] , 'nom': unTuple[1] , 'matricule': unTuple[0] }
		               
		
		reponse = json.dumps( uneConnexion )
	print "Rapports : " + reponse
	return Response( reponse , status=200 , mimetype='application/json' ) 

########################    RETOURNE LES VISITEURS ###########################

@app.route( '/visiteurs' , methods=['GET'] )
def getVisiteurs() :
	curseur = connexionBD.cursor()
	curseur.execute( 'SELECT VIS_MATRICULE, VIS_NOM, VIS_PRENOM, VIS_ADRESSE, VIS_CP, VIS_VILLE, CONVERT(VIS_DATEEMBAUCHE, CHAR), VIS_MDP FROM VISITEUR' )
	tuples = curseur.fetchall()
	curseur.close()
	lesVisiteurs = []
	for unTuple in tuples :
		unVisiteur = { 'Matricule': unTuple[0] , 'Nom': unTuple[1] , 'Prenom': unTuple[2] , 'Adresse': unTuple[3] , 'CP': unTuple[4] , 'Ville': unTuple[5] , 'Date d\'embauche': unTuple[6] , 'Mot de passe': unTuple[7] }
		lesVisiteurs.append( unVisiteur )
	reponse = json.dumps( lesVisiteurs )
	print "Rapports : " + reponse
	return Response( reponse , status=200 , mimetype='application/json' ) 
	
########################    RETOURNE LES VISITEURS POUR COMBOBOX ###########################

@app.route( '/cbVisiteurs' , methods=['GET'] )
def getCbVisiteurs() :
	curseur = connexionBD.cursor()
	curseur.execute( 'SELECT DISTINCT(LEFT(VIS_PRENOM,1)) AS VIS_PRENOM, VIS_NOM FROM VISITEUR' )
	tuples = curseur.fetchall()
	curseur.close()
	lesVisiteurs = []
	for unTuple in tuples :
		unVisiteur = { 'nom': unTuple[1] , 'prenom': unTuple[0] }
		lesVisiteurs.append( unVisiteur )
	reponse = json.dumps( lesVisiteurs )
	print "Rapports : " + reponse
	return Response( reponse , status=200 , mimetype='application/json' ) 

########################    RETOURNE LE VISITEUR CORRESPONDANT AU MATRICULE EN PARAMETRE ###########################

@app.route( '/visiteurs/<matricule>' , methods=['GET'] )
def getVisiteurParMatricule( matricule ) :
	curseur = connexionBD.cursor()
	curseur.execute( 'SELECT VIS_MATRICULE, VIS_NOM, VIS_PRENOM, VIS_ADRESSE, VIS_CP, VIS_VILLE, CONVERT(VIS_DATEEMBAUCHE, CHAR), VIS_MDP FROM VISITEUR WHERE VIS_MATRICULE = %s' , ( matricule , ) )
	tuples = curseur.fetchall()
	curseur.close()
	lesVisiteurs = []
	for unTuple in tuples :
		unVisiteur = { 'Matricule': unTuple[0] , 'Nom': unTuple[1] , 'Prenom': unTuple[2] , 'Adresse': unTuple[3] , 'CP': unTuple[4] , 'Ville': unTuple[5] , 'Date d\'embauche': unTuple[6] , 'Mot de passe': unTuple[7] }
		lesVisiteurs.append( unVisiteur )
	reponse = json.dumps( lesVisiteurs )
	print "Rapports : " + reponse
	return Response( reponse , status=200 , mimetype='application/json' ) 

########################    CHANGE LE MOT DE PASSE DU VISITEUR CORRESPONDANT AU MATRICULE EN PARAMETRE PAR LE MDP EN PARAMETRE ###########################

@app.route( '/visiteurs/changerMdp/<matricule>.<mdp>' , methods=['PUT'] )
def changerMdp( matricule , mdp ) :
	changerPwdJSON = request.data
	changerPwd = json.loads( changerPwdJSON )
	curseur = connexionBD.cursor()
	curseur.execute( 'UPDATE VISITEUR SET VIS_MDP = %s WHERE VIS_MATRICULE = %s' , ( mdp , matricule ) )
	idNouveauLivreur = curseur.lastrowid
	nbTuplesTraites = curseur.rowcount
	connexionBD.commit()

	curseur.close()
	
	reponse = make_response( '' )
	if nbTuplesTraites == 1 :
		reponse.mimetype = 'text/plain'
		reponse.status_code = 200
		
	else :
		pass
		reponse.mimetype = 'text/plain'
		reponse.status_code = 404
		
	return reponse 

########################    CHANGE LE MOT DE PASSE DU VISITEUR CORRESPONDANT AU MATRICULE EN PARAMETRE PAR LE MDP EN PARAMETRE ###########################
@app.route( '/rapports/estVu/<numRapport>' , methods=['PUT'] )
def estVu( numRapport ) :
	isViewedJSON = request.data
	isViewed = json.loads( isViewedJSON )
	curseur = connexionBD.cursor()
	curseur.execute( 'UPDATE RAPPORT_VISITE SET ESTVU = TRUE WHERE RAP_NUM = %s' , ( numRapport , ) )
	idNouveauLivreur = curseur.lastrowid
	nbTuplesTraites = curseur.rowcount
	connexionBD.commit()

	curseur.close()
	
	reponse = make_response( '' )
	if nbTuplesTraites == 1 :
		reponse.mimetype = 'text/plain'
		reponse.status_code = 200
		
	else :
		pass
		reponse.mimetype = 'text/plain'
		reponse.status_code = 404
		
	return reponse 


if __name__ == "__main__" :
	app.run( debug = True , host = '0.0.0.0' , port = 5000 )

