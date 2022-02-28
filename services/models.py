from django.db import models

SERVICE_CHOICE = [
    ('Project_writing_(thesis)', 'Research/project work (thesis)'),
    ('Data_Analysis', 'Data Analysis'),    
	('Content_Management', 'Content Management'),
    ('Web_Development', 'Web Development'),
        ('Others', 'Others'),
    ]

class Services(models.Model):
    name = models.CharField(help_text = 'Your full names', max_length=200)
    phone_number = models.CharField(help_text = 'phone number',max_length=20)
    email = models.EmailField()
    service = models.CharField(max_length=100,choices=SERVICE_CHOICE, default='Project_writing_(thesis)',
    help_text='Service required')
    description = models.TextField(blank=True, null=True, help_text='A brief description of the service requested')
