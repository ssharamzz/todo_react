from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from .models import Students, Scores
from .serializers import StudentSerializer, ScoreSerializer
from rest_framework.response import Response

# Create your views here.
# viewset 방식
class StudentView(ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer

    # http://127.0.0.1:8000/api/study/students/?name=홍길동
    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            qs = qs.filter(name=name)
        return qs
    
    # http://127.0.0.1:8000/api/study/students/incheon/
    # 함수명이 url
    @action(detail=False, methods=['GET'])
    def incheon(self, request):
        qs = self.get_queryset().filter(address__contains='인천') # like %인천%
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    # http://127.0.0.1:8000/api/study/students/7/init/
    # 7은 pk번호 넣는 부분, 입력받은 pk번호를 가지고 있는 학생의 주소와 이메일 정보가 초기화
    @action(detail=True, methods=['PUT'])
    def init(self, request, pk):
        instance = self.get_object()
        instance.address = ""
        instance.email = ""
        instance.save(update_fields=['address', 'email'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ScoreView(ModelViewSet):
    queryset = Scores.objects.all()
    serializer_class = ScoreSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        math = self.request.query_params.get('math')
        english = self.request.query_params.get('english')
        science = self.request.query_params.get('science')
        order = self.request.query_params.get('order')

        if name:
            qs = qs.filter(name=name)
        if math:
            qs = qs.filter(math__gte=math)
        if english:
            qs = qs.filter(english__gte=english)
        if science:
            qs = qs.filter(science__gte=science)
        if order:
            qs = qs.order_by(order)
        
        return qs
    
    @action(detail=False, methods=['GET'])
    def top(self, request):
        qs = self.get_queryset().filter(math__gte=80, english__gte=80, science__gte=80) # 각 과목의 점수가 80이상
        # 80이상 다른 쿼리문, 이 방법을 쓸 때는 from django.db.models import Q 해줘야 함
        # qs = self.get_queryset().filter(Q(math__gte=80) & Q(english__gte=80) & Q(science__gte=80)) 
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


# CBV 방식 APIView 상속
# class StudentView(APIView):
#     def get(self, request):
#         qs = Students.objects.all() # 메모리
#         serializer = StudentSerializer(qs, many=True) # 메모리(Object) > 텍스트
#         return Response(serializer.data) # 텍스트(JSON) 형태
#     def post(self, request):
#         serializer = StudentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class StudentDetailView(APIView):
#     def get_object(self, pk):
#         # return get_object_or_404(Students, pk=pk)
#         try:
#             student = Students.objects.get(pk=pk)
#         except:
#             raise Http404()
#         return student
#     def get(self, request, pk):
#         student = self.get_object(pk)
#         serializer = StudentSerializer(student)
#         return Response(serializer.data)
#     def put(self, request, pk):
#         student = self.get_object(pk)
#         print(request.data)
#         serializer = StudentSerializer(student, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#     def delete(self, request, pk):
#         student = self.get_object(pk)
#         student.delete()
#         return Response(status=204)

# class ScoreView(APIView):
#     def get(self, request):
#         qs = Scores.objects.all()
#         serializer = ScoreSerializer(qs, many=True)
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = ScoreSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
# class ScoreDetailView(APIView):
#     def get_object(self, pk):
#         # return get_object_or_404(Students, pk=pk)
#         try:
#             score = Scores.objects.get(pk=pk)
#         except:
#             raise Http404()
#         return score
#     def get(self, request, pk):
#         score = self.get_object(pk)
#         serializer = ScoreSerializer(score)
#         return Response(serializer.data)
#     def put(self, request, pk):
#         score = self.get_object(pk)
#         print(request.data)
#         serializer = ScoreSerializer(score, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#     def delete(self, request, pk):
#         score = self.get_object(pk)
#         score.delete()
#         return Response(status=204)


#FBV 방식 api_view 어노테이션 사용
# @api_view(['GET', 'POST'])
# def StudentView(request):
#     if request.method == 'GET':
#         qs = Students.objects.all()
#         serializer = StudentSerializer(qs, many=True) #qs의 결과가 list형이면 True, object형이면 False
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         # 직렬화 생성
#         serializer = StudentSerializer(data=request.data)
#         # validation 체크
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def StudentDetailView(request, id):
#     qs = get_object_or_404(Students, pk=id)

#     # 상세조회
#     if request.method == 'GET':
#         serializer = StudentSerializer(qs)
#         return Response(serializer.data)

#     # 수정
#     elif request.method == 'PUT':
#         serializer = StudentSerializer(qs, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     # 삭제
#     elif request.method == 'DELETE':
#         qs.delete()
#         return Response(status=204)


# @api_view(['GET', 'POST'])
# def ScoreView(request):
#     if request.method == 'GET':
#         qs = Scores.objects.all()
#         serializer = ScoreSerializer(qs, many=True) #qs의 결과가 list형이면 True, object형이면 False
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         # 직렬화 생성
#         serializer = ScoreSerializer(data=request.data)
#         # validation 체크
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def ScoreDetailView(request, id):
#     qs = get_object_or_404(Scores, pk=id)

#     # 상세조회
#     if request.method == 'GET':
#         serializer = ScoreSerializer(qs)
#         return Response(serializer.data)

#     # 수정
#     elif request.method == 'PUT':
#         serializer = ScoreSerializer(qs, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     # 삭제
#     elif request.method == 'DELETE':
#         qs.delete()
#         return Response(status=204)

