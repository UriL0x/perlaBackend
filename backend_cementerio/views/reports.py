from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Dceasced, Grave, Block, Section, Row
from ..reportSerializer import DeceasedSerializer, GraveSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from collections import defaultdict

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class GeneralReportView():
    @api_view(['GET'])
    def get(request):
        try:
            # Obtener todos los fallecidos
            deceased = Dceasced.objects.all()
            deceased_serialized = DeceasedSerializer(deceased, many=True).data

            # Obtener todas las tumbas con relaciones
            graves = Grave.objects.select_related('row__section__block').all()
            graves_serialized = GraveSerializer(graves, many=True).data

            # Mapear tumbas por fila para saber cuáles están ocupadas
            busy_rows = set(grave.row_id for grave in graves if grave.row_id is not None)

            # Estructura de resultado
            locations = defaultdict(lambda: defaultdict(list))

            # Obtener todas las filas con sus relaciones completas
            rows = Row.objects.select_related('section__block').all()

            for row in rows:
                if not row.section or not row.section.block:
                    continue

                block_num = row.section.block.num
                section_num = row.section.num
                row_num = row.num

                bloque_key = f"Bloque {block_num}"
                cuadro_key = f"Cuadro {section_num}"

                locations[bloque_key][cuadro_key].append(row_num)

            # Convertir defaultdicts a dicts normales y ordenar
            locations_dict = {
                bloque: {
                    cuadro: sorted(filas)
                    for cuadro, filas in cuadros.items()
                }
                for bloque, cuadros in locations.items()
            }

            return Response({
                'deceased': deceased_serialized,
                'graves': graves_serialized,
                'locations': locations_dict
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

