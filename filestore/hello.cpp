#include"myLighting.h"

Light myLightSrc[8];

void mySetLight(int id, int PROP, GLfloat* coef) {
	Light* light = &myLightSrc[id];
	switch (PROP) {
	case AMBIENT: light->ambient = coef; break;
	case DIFFUSION: light->diffuse = coef; break;
	case SPECULAR: light->specular = coef; break;
	case EMISSION: light->emission = coef; break;
	case POSITION: light->position = coef; break; // Light 구조체에 값을 넣는다.
	default: break;
	}
}

float myAttenuation(float ka, float kb, float kc, float distance) {
	float init = 1.0;
	float attenuationConst = ka * pow(distance, 2) + kb * distance + kc;  // 감쇠 상수 계산

	float intensity = init - attenuationConst;

	if (intensity < 0.0) { // 음수이면 0으로 고정
		intensity = 0.0;
	}
	return intensity;
}

void myAmbient(int id, GLfloat* coef) {
	Light* light = &myLightSrc[id];
	light->ambientValue = light->ambient[0] * coef[0] + light->ambient[1] * coef[1] + light->ambient[2] * coef[2] + light->ambient[3] * coef[3]; // ka * ia
}

void myDiffuse(int id, GLfloat* coef, GLfloat* normal_vec, GLfloat* position) {
	Light* light = &myLightSrc[id];
	GLfloat lightDir[3];
	for (int i = 0; i < 3; ++i) {
		lightDir[i] = light->position[i] - position[i]; // 광원과 물체 거리를 벡터로 만들기
	}

	GLfloat normalLen = std::sqrt(normal_vec[0] * normal_vec[0] + normal_vec[1] * normal_vec[1] + normal_vec[2] * normal_vec[2]); // 법선 벡터 거리
	GLfloat lightDirLen = std::sqrt(lightDir[0] * lightDir[0] + lightDir[1] * lightDir[1] + lightDir[2] * lightDir[2]); // 방금 만든 빛과 물체 사이 거리

	/*for (int i = 0; i < 3; ++i) {
		normal_vec[i] /= normalLen;
		lightDir[i] /= lightDirLen; // normalize 하기
	}*/
	GLfloat cosTheta = (normal_vec[0] * lightDir[0] + normal_vec[1] * lightDir[1] + normal_vec[2] * lightDir[2]) / (normalLen * lightDirLen); 
	// cos(theta) = 두 벡터의 dot 연산 / 두 벡터의 norm 곱

	light->diffuseValue = (light->diffuse[0] * coef[0] + light->diffuse[1] * coef[1] + light->diffuse[2] * coef[2] + light->diffuse[3] * coef[3]) * cosTheta;
	// kd * Id * cos(theta)
}

void mySpecular(int id, GLfloat* coef, GLfloat* normal_vec, GLfloat* position) {
	Light* light = &myLightSrc[id];
	GLfloat lightDir[3];
	for (int i = 0; i < 3; ++i) {
		lightDir[i] = light->position[i] - position[i]; // 광원과 물체 거리를 벡터로 만들기
	}

	GLfloat normalLen = std::sqrt(normal_vec[0] * normal_vec[0] + normal_vec[1] * normal_vec[1] + normal_vec[2] * normal_vec[2]); // 법선 벡터 거리
	GLfloat lightDirLen = std::sqrt(lightDir[0] * lightDir[0] + lightDir[1] * lightDir[1] + lightDir[2] * lightDir[2]); // 방금 만든 빛과 물체 사이 거리

	for (int i = 0; i < 3; ++i) { // normalize
		normal_vec[i] /= normalLen;
		lightDir[i] /= lightDirLen;
	}

	GLfloat reflection[3]; // R = 2 * (N * L) * N - L
	for (int i = 0; i < 3; ++i) {
		reflection[i] = 2 * (normal_vec[i] * lightDir[i]) * normal_vec[i] - lightDir[i];
	}

	GLfloat viewDir[3]; // 관찰자 방향 벡터 v
	for (int i = 0; i < 3; ++i) {
		viewDir[i] = -position[i];
	}

	GLfloat viewDirLen = sqrt(viewDir[0] * viewDir[0] + viewDir[1] * viewDir[1] + viewDir[2] * viewDir[2]);
	for (int i = 0; i < 3; ++i) {
		viewDir[i] /= viewDirLen; // 관찰자 방향 벡터 normalize
	}

	GLfloat specularIntensity = (light->specular[0] * coef[0] + light->specular[1] * coef[1] + light->specular[2] * coef[2] + light->specular[3] * coef[3])
		* pow(max(0.0f, reflection[0] * viewDir[0] + reflection[1] * viewDir[1] + reflection[2] * viewDir[2]), shininess_alpha); // specular 계산

	light->specularValue = fmax(0.0f, fmin(1.0f, specularIntensity)); // specularValue에 적재

}
void myLighting(int id) {
	Light* light = &myLightSrc[id];
	GLfloat atten = myAttenuation(1, 0, 0, 0.5); // 감쇠함수
	light->color[0] = atten * (light->ambientValue + light->diffuseValue + light->specularValue) + light->emission[0];
	light->color[1] = atten * (light->ambientValue + light->diffuseValue + light->specularValue) + light->emission[1];
	light->color[2] = atten * (light->ambientValue + light->diffuseValue + light->specularValue) + light->emission[2]; // 모든 변수 계산
}

void myDisplay_1() {
	GLfloat normal_vec[] = { 0, 0, 1 };
	GLfloat plane_pos[] = { 0, 0, 0 };
	GLfloat ambient_coef[] = { 1.0, 0.4, 0.4, 1.0 }; // Ia
	GLfloat diffuse_coef[] = { 1.0, 0.0, 0.0, 1.0 }; // Id
	GLfloat specular_coef[] = { 1.0, 0.0, 0.0, 1.0 }; // Is
	GLfloat light_pos[] = { 0.0, 0.0, -1.0, 1.0 };

	GLfloat emission_default[] = { 0.0, 0.0, 0.0, 1.0 }; // ke
	GLfloat ambient_default[] = { 0.2, 0.2, 0.2, 1.0 }; // ka
	GLfloat diffuse_default[] = { 0.8, 0.8, 0.8, 1.0 }; // kd
	GLfloat specular_default[] = { 0.0, 0.0, 0.0, 1.0 }; // ks

	mySetLight(MY_LIGHT0, AMBIENT, ambient_coef);
	mySetLight(MY_LIGHT0, DIFFUSION, diffuse_coef);
	mySetLight(MY_LIGHT0, SPECULAR, specular_coef);
	mySetLight(MY_LIGHT0, EMISSION, emission_default);
	mySetLight(MY_LIGHT0, POSITION, light_pos); // Light에 저장

	myAmbient(MY_LIGHT0, ambient_default);
	myDiffuse(MY_LIGHT0, diffuse_default, normal_vec, plane_pos);
	mySpecular(MY_LIGHT0, specular_default, normal_vec, plane_pos); //ambient, diffuse, specular 계산
	myLighting(MY_LIGHT0); // rgb 설정

	glClear(GL_COLOR_BUFFER_BIT);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	glRotatef(45, 1, 1, 0);
	glColor3f(myLightSrc[MY_LIGHT0].color[0], myLightSrc[MY_LIGHT0].color[1], myLightSrc[MY_LIGHT0].color[2]);
	glutSolidCube(0.5);
	glFlush();
}

int main(int argc, char** argv) {
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH);
	glutInitWindowSize(640, 480);
	glutCreateWindow("myLighting");
	glutDisplayFunc(myDisplay_1);
	glEnable(GL_LIGHTING); // 라이팅 켜기
	glEnable(GL_DEPTH_TEST); // 깊이 테스트 켜기
	glDepthFunc(GL_LESS);

	glutMainLoop();
	return 0;
}