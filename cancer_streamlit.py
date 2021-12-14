import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd 
from bravado.client import SwaggerClient

# This is the initialization of many of the data sources that we will need
cbioportal = cbioportal = SwaggerClient.from_url('https://www.cbioportal.org/api/api-docs', config={"validate_requests":False,"validate_responses":False,"validate_swagger_spec": False,})
studies = cbioportal.Studies.getAllStudiesUsingGET().result()
cancer_types = cbioportal.Cancer_Types.getAllCancerTypesUsingGET().result()


st.title('Cancer Genomics Portal')
st.markdown("""
This app highlights some mutations in various cancer types.
* The app is powered by the [Cancer Genomics Portal](https://www.cbioportal.org/)
* These mutations are collected by a collection of very talented researchers.
""")


def studies_response_to_dict(studies):
    studies_dict = []
    for study in studies:
        study_dict = {}
        study_dict['allSampleCount'] = study.allSampleCount
        study_dict['cancerType'] = study.cancerType
        study_dict['cancerTypeId'] = study.cancerTypeId
        study_dict['citation'] = study.citation
        study_dict['description'] = study.description
        study_dict['cnaSampleCount'] = study.cnaSampleCount
        study_dict['completeSampleCount'] = study.completeSampleCount
        study_dict['groups'] = study.groups
        study_dict['importDate'] = study.importDate
        study_dict['massSpectrometrySampleCount'] = study.massSpectrometrySampleCount
        study_dict['methylationHm27SampleCount'] = study.methylationHm27SampleCount
        study_dict['miRnaSampleCount'] = study.miRnaSampleCount
        study_dict['mrnaMicroarraySampleCount'] = study.mrnaMicroarraySampleCount
        study_dict['mrnaRnaSeqSampleCount'] = study.mrnaRnaSeqSampleCount
        study_dict['name'] = study.name
        study_dict['pmid'] = study.pmid
        study_dict['publicStudy'] = study.publicStudy
        study_dict['readPermission'] = study.readPermission
        study_dict['referenceGenome'] = study.referenceGenome
        study_dict['rppaSampleCount'] = study.rppaSampleCount
        study_dict['referenceGenome'] = study.referenceGenome
        study_dict['rppaSampleCount'] = study.rppaSampleCount
        study_dict['sequencedSampleCount'] = study.sequencedSampleCount
        study_dict['status'] = study.status
        study_dict['studyId'] = study.studyId
        studies_dict.append(study_dict)
    return studies_dict

studies_dict = studies_response_to_dict(studies)

st.write('Studes overview:')
df = pd.DataFrame(studies_dict)

df