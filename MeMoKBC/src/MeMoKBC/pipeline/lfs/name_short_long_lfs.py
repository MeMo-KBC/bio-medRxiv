from fonduer.utils.data_model_utils.visual import get_page_vert_percentile
from snorkel.labeling import labeling_function
from pathlib import Path
import csv

ABSTAIN = -1
FALSE = 0
TRUE = 1

@labeling_function()
def name_short_outside_half_percentile(c):
    '''Checks if name short is in the lower half of the document'''
    name_short, name_full = c
    try:
        short_vert_percentile = get_page_vert_percentile(name_short)
    except:
        print(c)
        return ABSTAIN
    if short_vert_percentile >= 0.5:
        return TRUE
    else:
        return ABSTAIN
 
 
@labeling_function()
def name_full_in_top_percentile(c):
    '''Checks if name long is in the top percentile of the document'''
    name_short, name_full = c
    full_vert_percentile = get_page_vert_percentile(name_full)
    if full_vert_percentile <= 0.25:
        return TRUE
    else:
        return ABSTAIN



def get_page_vert_perc_by_sentence(mention):
    '''Returns the vertical percentile of a mention by sentence'''
    sentence = mention.context.sentence
    sentences = mention.context.sentence.document.sentences
    return sentences.index(sentence) / len(sentences) 

@labeling_function()
def name_short_outside_half_percentile_sentence_wise(c):
    '''Checks if name short is in the lower half of the documents sentences'''
    name_short, name_full = c
    try:
        short_vert_percentile = get_page_vert_perc_by_sentence(name_short)
    except:
        print(c)
        return ABSTAIN
    
    if short_vert_percentile >= 0.5:
        return TRUE
    else:
        return ABSTAIN
    
@labeling_function()
def is_company_name(c):
    name_short, name_full  = c
    name = name_full.context.get_span()

    word_list = []
    with open(f'{str(Path(__file__).parent)}/CSVs/Company_Abbr.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word_list.extend(row)
    
    name_lower = name.lower()
    for word in word_list:
        if word.lower() in name_lower:
            return FALSE
    return ABSTAIN
    
@labeling_function()
def name_full_in_top_percentile_sentence_wise(c):
    '''Checks if name long is in the top percentile of the document'''
    name_short, name_full = c
    full_vert_percentile = get_page_vert_perc_by_sentence(name_full)
    if full_vert_percentile <= 0.25:
        return TRUE
    else:
        return ABSTAIN


@labeling_function()
def word_count(c):
    '''Checks if name short has less than or equal to 8 letters'''
    name_short, name_full = c
    short_string = name_short.context.get_span()
   
    if len(short_string) <= 8:
        return TRUE
    else:
        return ABSTAIN
    

@labeling_function()
def small_letter_count(c):
    '''Checks if name short has less than or equal to 2 small letters'''
    name_short, name_full = c
    name_short_string = name_short.context.get_span()
    lowercase_count = sum(1 for w in name_short_string if w.islower())

    if lowercase_count <= 2:
        return TRUE
    else:
        return ABSTAIN


@labeling_function()
def check_all_uppercase_letters(c):
    '''Checks if all name short uppercase letters are in name long'''
    name_short, name_full = c
    
    short_string = name_short.context.get_span()
    long_string = name_full.context.get_span() 
    
    uppercase_set = set(char for char in long_string if char.isupper())

    letters = ''.join(char for char in short_string if char.isalpha() and char.isupper())


    for letter in letters:
        if letter not in uppercase_set:
            return ABSTAIN
    
    return TRUE

@labeling_function()
def check_uppercase_letters(c):
    name_short = c[0]
    name_long = c[1]
    
    short_string = name_short.context.get_span()
    long_string = name_long.context.get_span()
    
    short_letters = [char for char in short_string if char.isupper()]
    long_letters = [char for char in long_string if char.isupper()]
    
    pattern_index = 0
    
    for letter in long_letters:
        if letter == short_letters[pattern_index]:
            pattern_index += 1
            
            if pattern_index == len(short_letters):
                return TRUE
                
    return ABSTAIN

@labeling_function()
def check_horizont_abr_short(c):
    name_short, name_full = c
    short_string = name_short.context.get_span()

    horizont_list = ["AAL","ACARE", "ACCESS4EU", "ACP", "AdG", "AdR", "ALICE", "AEUV", "AKP", "Artemis",
                     "AStV", "BAK", "BBI", "BILAT", "BMBF", "BONUS", "BRIC(S)", "BtR", "CAD", "CAF", "CAP",
                     "CBRNE", "CEEC", "CFS", "CFSP", "CIP", "CNECT", "COFUND", "CoG", "COM", "CoMAv",
                     "CORDIS", "COREPER", "CRM", "cPPP", "CRP", "COSME", "COST", "CSA", "CSA-ERA-Plus", "CSF",
                     "CSO", "DEM", "DESCA", "DFG", "DG Connect", "DG EAC", "DG ENTR", "DG SANTE", "DG RTD", "DMP", "DoA", "DoW",
                     "EAG", "EARPA", "EASME", "ECORDA", "ECSC", "ECSEL", "ECTRI", "EDCTP", "EEA", "EEA", "EeB", "EECA",
                     "EEIG", "EEN", "EFR", "EFRE", "EFTA", "EGNSS", "EGKS", "EGV", "EGVI", "EHHO", "EIB", "EIC",
                     "EID", "EIF", "EIP", "EIT", "EJD", "EJP", "EMIRI", "EMN", "EMM", "EMRP", "EMU", "ENIAC", "ENV",
                     "ERA", "ERAB", "ERAC", "ERA NET", "ERC", "ERC-AdG", "ERC-CoG", "ERC-PoC", "ERC-StG", "ERC-SyG",
                     "ERCEA", "ERDF", "ERRAC", "ERTICO", "ERTMS", "ERTRAC", "ESF", "ESFRI", "ESIF", "ESO", "ESR", "ESR",
                     "ESRF", "ETN", "ETP", "EUCAR", "EUGH", "EURAM", "Euratom", "EURAXESS", "EuroHPC", "EWR", "EWSA",
                     "F&I", "F&T Portal", "FCH JU", "FET", "FiF", "FIS", "Form C", "FoF", "FPA", "FRP", "FSign",
                     "FTE", "FTI", "FuE", "GAP", "GASP", "GÉANT", "GFS", "GMES", "GPC", "GPF", "GWK",
                     "H2020", "HERA", "HES", "hESC", "HEU", "HIP", "HLG", "HPC", "IAM", "ICPC", "ICT", "IESBA", "IGLO", "IKT",
                     "IMI", "INCO", "INEA", "IOR", "IoT", "IPR", "IRE", "ISC", "ITER", "ITN", "ITRE", "JPI",
                     "JPI CH", "JPI MYBL", "JPND", "JRC", "JTI", "KET", "KIC", "KMU", "KOM", "KoWi",
                     "LEAR", "LEIT", "LoI", "LSign", "MGA", "MGT", "MOEL", "MoU", "MPC", "MSCA",
                     "MSC-COFUND", "MSC-IF", "MSC-ITN", "MSC-RISE", "MST", "NanoMatPro", "NCP", "NDA", "NEF", "Net4Society",
                     "NIGHT", "NGO", "NKS", "NMP", "NORFACE", "OLAF", "OTH", "P2P", "PCP", "PDM",
                     "PFSIGN", "PGA", "PIC", "PLSIGN", "PMNI", "PoC", "PPI", "PPP", "PPSS", "PRIMA", "PSF", "PUB", "R&I", "RAG",
                     "REA", "REC", "RIA", "RIS3", "RISE", "RRI", "RTD", "RTDI", "S&T", "SCAR", "SDG", "SEP", "SESAR",
                     "SET -Plan", "SFIC", "SIA", "SME", "SPIRE", "SRA", "SRIA", "SRC", "SSA", "SSC", "SSF", "SSH",
                     "StäV", "StG", "STRIA", "SUMP", "SwafS", "SWG", "SUPP", "SyG", "TEN", "TFEU", "ToR", "TRIMIS", "TRL",
                     "TTG", "URF", "VZA", "WBC", "WEU", "WTZ", "WWU", "ZIM"]
    
    if short_string in horizont_list:
        return FALSE
    else:
        return ABSTAIN
    

@labeling_function()
def check_uppercase_letters_short_in_long(c):
    name_short, name_full = c
    
    short_string = name_short.context.get_span()
    long_string = name_full.context.get_span()
    
    short_letters = [char for char in short_string if char.isupper()]
    long_letters = [char for char in long_string if char.isupper()]
    
    pattern_index = 0
    
    for letter in long_letters:
        if letter == short_letters[pattern_index]:
            pattern_index += 1
            
            if pattern_index == len(short_letters):
                return TRUE
                
    return ABSTAIN


@labeling_function()
def check_long_name_not_upper(c):
    name_short, name_full = c
    long_string = name_full.context.get_span()
    
    words = long_string.split()
    
    for word in words:
        uppercase_count = sum(1 for letter in word if letter.isupper())
        if uppercase_count >= 2:
            return FALSE
    
    return ABSTAIN




short_long_lfs = [
    # name_short_outside_half_percentile,
    name_short_outside_half_percentile_sentence_wise,
    # name_full_in_top_percentile,
    name_full_in_top_percentile_sentence_wise,
    word_count,
    small_letter_count,
    check_all_uppercase_letters,
    check_uppercase_letters,
    check_horizont_abr_short,
    check_uppercase_letters_short_in_long,
    check_long_name_not_upper
]