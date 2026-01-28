from django.db import models

class Inscription(models.Model):
    FORMATIONS = [
        ('SEC_BUR', 'Secrétariat Bureautique et Maintenance'),
        ('INFOG', 'Infographie et Motion Design'),
        ('DEV_WEB', 'Développement Web et Mobile'),
        ('IA_SYS', 'Intelligence Artificielle et Système Intelligent'),
    ]

    nom_parent = models.CharField(max_length=100)
    email_parent = models.EmailField()
    tel_parent = models.CharField(max_length=20)
    nom_eleve = models.CharField(max_length=100)
    formation = models.CharField(max_length=10, choices=FORMATIONS)
    capture_paiement = models.ImageField(upload_to='paiements/')
    date_inscription = models.DateTimeField(auto_now_add=True)
    valide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom_eleve} - {self.formation}"
