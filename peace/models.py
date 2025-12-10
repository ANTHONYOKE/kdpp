from django.db import models

# =====================
# REPORT MODEL (GDPP)
# =====================
class Report(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100)          # Kenya region
    county = models.CharField(max_length=100)          # County in Kenya
    case_type = models.CharField(max_length=100)       # Type of case (Conflict, Violence, etc.)
    description = models.TextField()                   # Incident description
    image = models.FileField(upload_to='reports/', blank=True, null=True)
    anonymous = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)

    # ---- AI ANALYSIS FIELDS ----
    severity = models.CharField(max_length=20, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.anonymous:
            return f"Anonymous Report - {self.case_type} ({self.county})"
        return f"{self.name or 'No Name'} - {self.case_type} ({self.county})"
