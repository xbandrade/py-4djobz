from django.utils.translation import gettext_lazy as _

SALARY_CHOICES = [
    ('< $1000', '< $1000'),
    ('$1000 - $2000', '$1000 - $2000'),
    ('$2000 - $3000', '$2000 - $3000'),
    ('> $3000', '> $3000'),
]
MIN_EDUCATION_CHOICES = [
    (_('Elementary School'), _('Elementary School')),
    (_('High School'), _('High School')),
    (_('Technologist'), _('Technologist')),
    (_('College Graduation'), _('College Graduation')),
    (_("MBA/Master's degree"), _("MBA/Master's degree")),
    (_('PhD/Doctorate degree'), _('PhD/Doctorate degree')),
]


def is_salary_compatible(applicant_expectation, job_salary):
    if applicant_expectation == job_salary:
        return True
    try:
        expectation_index = SALARY_CHOICES.index(
            (applicant_expectation, applicant_expectation))
        job_salary_index = SALARY_CHOICES.index((job_salary, job_salary))
        return expectation_index <= job_salary_index
    except ValueError:
        return False


def is_education_compatible(applicant_education, job_education):
    if applicant_education == job_education:
        return True
    try:
        applicant_education_index = MIN_EDUCATION_CHOICES.index(
            (applicant_education, applicant_education))
        job_education_index = MIN_EDUCATION_CHOICES.index(
            (job_education, job_education))
        return applicant_education_index >= job_education_index
    except ValueError:
        return False
