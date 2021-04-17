from django.db import models
from django.utils.translation import gettext_lazy as _
import string, secrets

class CleanCharField(models.CharField):
    """
    Helper CharField:
        (1) with leading/trailing white spaces trimmed;
        (2) with extra white spaces between words trimmed;
        (3) converted to title format (first letter of each word capitalized).
    """
    def __init__(self, *args, **kwargs):
        self.max_length = kwargs['max_length']
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        att = getattr(model_instance, self.attname)
        return ' '.join(att.split()).title()

class Gender(models.TextChoices):
    F = 'F', _('Female')
    M = 'M', _('Male')
    X = 'X', _('Non binary')

class Race(models.TextChoices):
    A = 'A', _('American Indian/Alaskan Native')
    S = 'S', _('Asian')
    B = 'B', _('Black/African American')
    P = 'P', _('Native Hawaiian/Other Pacific Islander')
    W = 'W', _('White')
    O = 'O', _('Other Race')
    X = 'X', _('Prefer not to specify')

class Ethnicity(models.TextChoices):
    H = 'H', _('Hispanic')
    N = 'N', _('Non-hispanic')
    X = 'X', _('Prefer not to specify')

class AddressType(models.TextChoices):
    H = 'H', _('Home')
    C = 'C', _('Current/Temporary')
    P = 'P', _('Permanet')
    M = 'M', _('Mailing')

class States(models.TextChoices):
    AL = 'AL', _('Alabama')
    AK = 'AK', _('Alaska')
    AS = 'AS', _('American Samoa')
    AZ = 'AZ', _('Arizona')
    AR = 'AR', _('Arkansas')
    CA = 'CA', _('California')
    CO = 'CO', _('Colorado')
    CT = 'CT', _('Connecticut')
    DE = 'DE', _('Delaware')
    DC = 'DC', _('District of Columbia')
    FL = 'FL', _('Florida')
    GA = 'GA', _('Georgia')
    GU = 'GU', _('Guam')
    HI = 'HI', _('Hawaii')
    ID = 'ID', _('Idaho')
    IL = 'IL', _('Illinois')
    IN = 'IN', _('Indiana')
    IA = 'IA', _('Iowa')
    KS = 'KS', _('Kansas')
    KY = 'KY', _('Kentucky')
    LA = 'LA', _('Louisiana')
    ME = 'ME', _('Maine')
    MD = 'MD', _('Maryland')
    MA = 'MA', _('Massachusetts')
    MI = 'MI', _('Michigan')
    MN = 'MN', _('Minnesota')
    MS = 'MS', _('Mississippi')
    MO = 'MO', _('Missouri')
    MT = 'MT', _('Montana')
    NE = 'NE', _('Nebraska')
    NV = 'NV', _('Nevada')
    NH = 'NH', _('New Hampshire')
    NJ = 'NJ', _('New Jersey')
    NM = 'NM', _('New Mexico')
    NY = 'NY', _('New York')
    NC = 'NC', _('North Carolina')
    ND = 'ND', _('North Dakota')
    MP = 'MP', _('Northern Mariana Islands')
    OH = 'OH', _('Ohio')
    OK = 'OK', _('Oklahoma')
    OR = 'OR', _('Oregon')
    PA = 'PA', _('Pennsylvania')
    PR = 'PR', _('Puerto Rico')
    RI = 'RI', _('Rhode Island')
    SC = 'SC', _('South Carolina')
    SD = 'SD', _('South Dakota')
    TN = 'TN', _('Tennessee')
    TX = 'TX', _('Texas')
    UT = 'UT', _('Utah')
    VT = 'VT', _('Vermont')
    VI = 'VI', _('Virgin Islands')
    VA = 'VA', _('Virginia')
    WA = 'WA', _('Washington')
    WV = 'WV', _('West Virginia')
    WI = 'WI', _('Wisconsin')
    WY = 'WY', _('Wyoming')

class MedicalQuestionType(models.TextChoices):
    S = 'S', _('Screening')
    E = 'E', _('Eligibility')

def GenerateDBID():
    excluded = ["I", "O", "0", "1"]
    alphabet = [*filter(lambda x: x not in excluded, string.ascii_uppercase + string.digits )]
    dbid = '-'.join(''.join(secrets.choice(alphabet) for i in range(3)) for i in range(3))
    return dbid