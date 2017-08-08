```
class CrearUsuarioCorreoAPIView(CreateAPIView):
    def get_serializer_class(self):
        return UserSerializer

    def create(self, request, *args, **kwargs):
        email = User.objects.filter(email=request.data.get('email'))
        username = User.objects.filter(username=request.data.get('username'))
        if not email.exists():
            if not username.exists():
                try:
                    contrasena = User.objects.make_random_password(length=8)
                    usuario = User.objects.create(
                        username=request.data.get('username'),
                        email=request.data.get('email'),
                        password=make_password(contrasena),
                        is_active=True,
                    )
                    perfil = UsuarioPerfil.objects.create(
                        user=usuario,
                        telefono=request.data.get('telefono')
                    )
                    g = Group.objects.get(name='Web')
                    g.user_set.add(usuario)
                    html = '<div class="contendedor"><h2 class="header"><img alt="Gobierno ' \
                           'del estado de Tabasco" src="https://registrociviladmin.tabasco.gob.mx/static/img/logos.png"' \
                           'style="max-width: 300px; height: auto;" /> ' \
                           '</h2><h3 class="header">Registro Civil</h3><p><b>Usuario creado exitosamente' \
                           '</b></p><p>Para acceder por primera vez, visite la siguiente dirección: <strong><a ' \
                           'href="http://registrocivil.tabasco.gob.mx/"><a href="https://registrocivil.tabasco.gob.mx/">' \
                           '<ahref="https://registrocivil.tabasco.gob.mx/">https://registrocivil.tabasco.gob.mx/</a></a></a></strong>' \
                           '</p><p>Escriba su usuario y la contraseña provisional, una vez iniciada la sesión, podrá cambiar su ' \
                           'contraseña.</p><ul><li><strong>Usuario:</strong> <em>{}</em></li><li><strong>Contraseña ' \
                           'provisional:</strong> <em>{}</em></li></ul></div>'.format(self.request.data['username'],
                                                                                      contrasena)
                    msg = EmailMultiAlternatives('Datos de acceso Sistema de Registro Civil', '', EMAIL_HOST_USER,
                                                 [self.request.data['email']])
                    msg.attach_alternative(html, "text/html")
                    msg.send()
                    data = {
                        'code': '01',
                        'message': 'El registro se ha creado exitosamente, revise en su correo electronico los datos para poder acceder al sistema.',
                        'description': 'Usuario id: {} creado'.format(usuario.pk)
                    }
                    estado = status.HTTP_200_OK
                except Exception as error:
                    data = {
                        'code': '03',
                        'message': 'No fue posible crear el usuario, contacte con el administrador',
                        'description': 'Error: {}'.format(error)
                    }
                    estado = status.HTTP_404_NOT_FOUND
            else:
                data = {
                    'code': '02',
                    'message': 'Ya existe un usuario {}.'.format(request.data.get('username')),
                    'description': 'Ya existe un usuario {}.'.format(request.data.get('username'))
                }
                estado = status.HTTP_409_CONFLICT
        else:
            data = {
                'code': '02',
                'message': 'Ya existe un usuario relacionado al correo electronico {}.'.format(
                    request.data.get('email')),
                'description': 'Ya existe un usuario con correo {}.'.format(request.data.get('email'))
            }
            estado = status.HTTP_409_CONFLICT
        return Response(data=data, status=estado)
```
