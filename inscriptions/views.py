# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Inscription
from reportlab.pdfgen import canvas
import urllib.parse

def formulaire_inscription(request):
    if request.method == 'POST':
        # Récupération des données du formulaire
        nouvelle_ins = Inscription.objects.create(
            nom_parent=request.POST['nom_parent'],
            email_parent=request.POST['email_parent'],
            tel_parent=request.POST['tel_parent'],
            nom_eleve=request.POST['nom_eleve'],
            formation=request.POST['formation'],
            capture_paiement=request.FILES['capture_paiement']
        )
        
        # Préparation du lien WhatsApp (Etape 3)
        numero_responsable = "237696864280" # Remplacez par votre numéro
        message = f"Bonjour, j'ai inscrit {nouvelle_ins.nom_eleve} en {nouvelle_ins.get_formation_display()}. Voici ma preuve de paiement."
        msg_encode = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/{numero_responsable}?text={msg_encode}"
        
        return redirect(whatsapp_url)
        
    return render(request, 'inscriptions/formulaire.html')

def generer_pdf(request, id):
    ins = Inscription.objects.get(id=id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="recu_{ins.nom_eleve}.pdf"'
    
    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "EMMERGENCE ACADEMIQUE - REÇU")
    p.setFont("Helvetica", 12)
    p.drawString(100, 750, f"Parent: {ins.nom_parent}")
    p.drawString(100, 730, f"Élève: {ins.nom_eleve}")
    p.drawString(100, 710, f"Formation: {ins.get_formation_display()}")
    p.drawString(100, 690, "Statut: INSCRIPTION VALIDÉE")
    p.showPage()
    p.save()
    return response