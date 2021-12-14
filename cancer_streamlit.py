import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd 
from bravado.client import SwaggerClient

# This is the initialization of many of the data sources that we will need
cbioportal = cbioportal = SwaggerClient.from_url('https://www.cbioportal.org/api/api-docs', 
    config={"validate_requests":False,"validate_responses":False,"validate_swagger_spec": False,})
#Fetch all of the studies
studies = cbioportal.Studies.getAllStudiesUsingGET().result()

#Limit the cancer types to only those that have studies
study_cancer_types = [cancer_ids.cancerTypeId for cancer_ids in studies]
cancer_types = cbioportal.Cancer_Types.getAllCancerTypesUsingGET().result()
cancer_types_filtered = [cancer_object for cancer_object in cancer_types if cancer_object.cancerTypeId in study_cancer_types]

st.title('Cancer Genomics Portal')
st.markdown("""
This app highlights some mutations in various cancer types.
* The app is powered by the [Cancer Genomics Portal](https://www.cbioportal.org/)
* These mutations are collected by a collection of very talented researchers.
""")
st.sidebar.header('Cancer Filters/Types')

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
studies_df = pd.DataFrame(studies_dict)

#Built the sidebar
cancer_type_names = {cancer_type.name for cancer_type in cancer_types_filtered}
selected_cancer_type_two = st.sidebar.selectbox('Cancer Type Name', cancer_type_names)

#selection logic for the creation of the dataframe
st.write(selected_cancer_type_two)
cancer_object = [c for c in cancer_types if c.name == selected_cancer_type_two][0]
df_selected_cancer_studies = studies_df[studies_df['cancerTypeId'] == cancer_object.cancerTypeId]
st.write('Studes overview:')
st.dataframe(df_selected_cancer_studies)