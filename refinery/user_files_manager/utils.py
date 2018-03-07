from django.conf import settings
from django.contrib.auth.models import User

from core.utils import get_resources_for_user
from data_set_manager.models import Assay, AttributeOrder, Study
from data_set_manager.search_indexes import NodeIndex
from data_set_manager.serializers import AttributeOrderSerializer
from data_set_manager.utils import generate_solr_params


def generate_solr_params_for_user(params, user_id):
    """Creates the encoded solr params limiting results to one user.
    Keyword Argument
        params -- python dict or QueryDict
    Params/Solr Params
        is_annotation - metadata
        facet_count/facet - enables facet counts in query response, true/false
        offset - paginate, offset response
        limit/row - maximum number of documents
        field_limit - set of fields to return
        facet_field - specify a field which should be treated as a facet
        facet_filter - adds params to facet fields&fqs for filtering on fields
        facet_pivot - list of fields to pivot
        sort - Ordering include field name, whitespace, & asc or desc.
        fq - filter query
     """

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        user = User.get_anonymous()

    datasets = get_resources_for_user(user, "dataset")

    assay_uuids = []

    for dataset in datasets:
        investigation_link = dataset.get_latest_investigation_link()
        if investigation_link is None:
            continue
            # It's not an error not to have data,
            # but there's nothing more to do here.
        investigation = investigation_link.investigation

        study_ids = Study.objects.filter(
            investigation=investigation
        ).values_list('id', flat=True)

        assay_uuids += Assay.objects.filter(
            study_id__in=study_ids
        ).values_list('uuid', flat=True)
        # Missing facet_fields, it is generated from Attribute Order Model.
        attributes_str = AttributeOrder.objects.filter(
            assay__uuid__in=assay_uuids
        )

        attributes = AttributeOrderSerializer(attributes_str, many=True)

        facet_template_char = '{0}_Characteristics{1}'
        facet_template_fac = '{0}_Factor_Value{1}'

        config_facets = settings.USER_FILES_FACETS.split(",")
        pivot_facets = {}

        # filter though attributes & keep the user files related attribute name
        for facet_name in config_facets:
            facet_char_generic_name = facet_template_char.format(
                facet_name,
                NodeIndex.GENERIC_SUFFIX
            )
            facet_fac_generic_name = facet_template_fac.format(
                facet_name,
                NodeIndex.GENERIC_SUFFIX
            )
            pivot_facets[facet_char_generic_name] = []
            pivot_facets[facet_fac_generic_name] = []
            # check if config facet needs a pivot
            # { org_char_generic: [org_char_1, org_char_2],
            # type_char_generic: [type_char_1, type_char_2]  }
            for attribute_obj in attributes.data:
                attribute_name = attribute_obj.get('solr_field')
                if attribute_name.startswith(''.join(
                        [facet_name, '_Characteristics']
                )) and attribute_name != facet_char_generic_name:
                    pivot_facets[facet_char_generic_name].append(
                        attribute_obj.get('solr_field')
                    )
                if attribute_name.startswith(''.join(
                        [facet_name, '_Factor_Value']
                )) and attribute_name != facet_fac_generic_name:
                    pivot_facets[facet_fac_generic_name].append(
                        attribute_obj.get('solr_field'))

    return generate_solr_params(params,
                                assay_uuids=assay_uuids,
                                facets_from_config=True)
