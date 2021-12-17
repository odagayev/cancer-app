import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd 
from bravado.client import SwaggerClient
from pprint import pprint

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

def get_mutations_for_study(study_id):
    mutations_profileID = study_id + '_mutations'
    sampleListId = study_id + '_all'
    mutations = cbioportal.Mutations.getMutationsInMolecularProfileBySampleListIdUsingGET(
        molecularProfileId=mutations_profileID,
        sampleListId=sampleListId,
        projection='DETAILED'
    ).result()
    return mutations

def get_mutations_from_study_list(study_list):
    mutations_list = []
    for study in study_list:
        mutations = get_mutations_for_study(study)
        mutations_list.append(mutations)
    return mutations_list

def mutatations_response_to_dict(mutations):
    mutation_dicts = []
    for mutation in mutations:
        mutation_dict = {}
        mutation_dict['alleleSpecificCopyNumber'] = mutation.alleleSpecificCopyNumber
        mutation_dict['aminoAcidChange'] = mutation.aminoAcidChange
        mutation_dict['center'] = mutation.center
        mutation_dict['chr'] = mutation.chr
        mutation_dict['driverFilter'] = mutation.driverFilter
        mutation_dict['driverFilterAnnotation'] = mutation.driverFilterAnnotation
        mutation_dict['driverTiersFilter'] = mutation.driverTiersFilter
        mutation_dict['driverTiersFilterAnnotation'] = mutation.driverTiersFilterAnnotation
        mutation_dict['endPosition'] = mutation.endPosition
        mutation_dict['entrezGeneId'] = mutation.entrezGeneId
        mutation_dict['fisValue'] = mutation.fisValue
        mutation_dict['functionalImpactScore'] = mutation.functionalImpactScore
        mutation_dict['gene_obj'] = mutation.gene
        mutation_dict['gene_str'] = str(mutation.gene) #this is a string version for the dataframe
        mutation_dict['keyword'] = mutation.keyword
        mutation_dict['linkMsa'] = mutation.linkMsa
        mutation_dict['linkPdb'] = mutation.linkPdb
        mutation_dict['linkXvar'] = mutation.linkXvar
        mutation_dict['molecularProfileId'] = mutation.molecularProfileId
        mutation_dict['mutationStatus'] = mutation.mutationStatus
        mutation_dict['mutationType'] = mutation.mutationType
        mutation_dict['namespaceColumns'] = mutation.namespaceColumns
        mutation_dict['ncbiBuild'] = mutation.ncbiBuild
        mutation_dict['normalAltCount'] = mutation.normalAltCount
        mutation_dict['normalRefCount'] = mutation.normalRefCount
        mutation_dict['patientId'] = mutation.patientId
        mutation_dict['proteinChange'] = mutation.proteinChange
        mutation_dict['proteinPosEnd'] = mutation.proteinPosEnd
        mutation_dict['proteinPosStart'] = mutation.proteinPosStart
        mutation_dict['referenceAllele'] = mutation.referenceAllele
        mutation_dict['refseqMrnaId'] = mutation.refseqMrnaId
        mutation_dict['sampleId'] = mutation.sampleId
        mutation_dict['startPosition'] = mutation.startPosition
        mutation_dict['studyId'] = mutation.studyId
        mutation_dict['tumorAltCount'] = mutation.tumorAltCount
        mutation_dict['tumorRefCount'] = mutation.tumorRefCount
        mutation_dict['uniquePatientKey'] = mutation.uniquePatientKey
        mutation_dict['uniqueSampleKey'] = mutation.uniqueSampleKey
        mutation_dict['validationStatus'] = mutation.validationStatus
        mutation_dict['variantAllele'] = mutation.variantAllele
        mutation_dict['variantType'] = mutation.variantType
        mutation_dicts.append(mutation_dict)
    return mutation_dicts


studies_dict = studies_response_to_dict(studies)
studies_df = pd.DataFrame(studies_dict)

#Built the sidebar
cancer_type_names = {cancer_type.name for cancer_type in cancer_types_filtered}
selected_cancer_type_two = st.sidebar.selectbox('Cancer Type Name', cancer_type_names)
st.write(selected_cancer_type_two)


#selection logic for the creation of the dataframe

cancer_object = [c for c in cancer_types if c.name == selected_cancer_type_two][0]
df_selected_cancer_studies = studies_df[studies_df['cancerTypeId'] == cancer_object.cancerTypeId]
mutations_from_studies_list = df_selected_cancer_studies['studyId'].to_list()
#print(mutations_from_studies_list)

st.write('Studes overview:')
st.dataframe(df_selected_cancer_studies)

#print(df_selected_cancer_studies.head(1))

study_mutations = get_mutations_for_study(df_selected_cancer_studies.studyId.iloc[0])
mutations_study_list = get_mutations_from_study_list(mutations_from_studies_list)
study_mutations = mutatations_response_to_dict(study_mutations)

study_mutations_df = pd.DataFrame(study_mutations)
study_mutations_df = study_mutations_df.drop(columns=['gene_obj']) # have to drop this because object is not JSON serializable

st.write('Mutations present:')
st.dataframe(study_mutations_df)