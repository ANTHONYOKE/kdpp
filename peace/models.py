from django.db import models

# =====================
# CONTACT MODEL
# =====================
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name


# =====================
# REPORT MODEL (GDPP)
# =====================
class Report(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    evidence = models.FileField(upload_to='evidence/', blank=True, null=True)
    anonymous = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.anonymous:
            return f"Anonymous Report - {self.category} ({self.location})"
        return f"{self.name or 'No Name'} - {self.category} ({self.location})"

class Report(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    evidence = models.FileField(upload_to='evidence/', blank=True, null=True)
    anonymous = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)

    # ---- AI FIELDS ----
    ai_severity = models.CharField(max_length=20, blank=True, null=True)
    ai_summary = models.TextField(blank=True, null=True)
    keywords_detected = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.anonymous:
            return f"Anonymous Report - {self.category} ({self.location})"
        return f"{self.name or 'No Name'} - {self.category} ({self.location})"
