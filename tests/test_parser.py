from project.parser import check_parser_correct, generate_dot_str
from textwrap import dedent


def test_empty():
    assert check_parser_correct("")


def test_not_belongs():
    assert not check_parser_correct("something")
    assert not check_parser_correct("print")
    assert not check_parser_correct("let =a ")
    assert not check_parser_correct("{10 {}{}")
    assert not check_parser_correct('g1 = load "wine.dot"')


def test_print():
    assert check_parser_correct("print 1;")
    assert check_parser_correct("print {1..10};")
    assert check_parser_correct("print {1, 2, 3, 10};")
    assert check_parser_correct('print load "wine.dot";')


def test_bind():
    assert check_parser_correct("let x = 1;")
    assert check_parser_correct("let x = {1..10};")
    assert check_parser_correct("let x = {1, 2, 3, 5};")
    assert check_parser_correct('let g1 = load "wine.dot";')


def test_lambda():
    assert check_parser_correct("let res = map (get_edges g) with g => g;")
    assert check_parser_correct("let res = filter (get_edges g) with g => g;")
    assert not check_parser_correct("let res = g => g")
    assert not check_parser_correct("g => g => g;")


example1 = """let g1 = load "wine.dot";
let g = set_start {0..100} of (set_final (get_vertices g1) of g1);

let l1 = "l1" | "l2";
let q1 = ("type" | l1)*;


let q2 = "sub_class_of" + l1;

let res1 = g & q1;
let res2 = g & q2;


print res1;

let s = get_start g;

let vertices1 = filter (map (get_edges res1) with ((u_g, u_q1), l, (v_g, v_q1)) => u_g) with v => v in s;
let vertices2 = filter (map (get_edges res2) with ((u_g, u_q2), l, (v_g, v_q2)) => u_g) with (v => v in s);

let vertices = vertices1 & vertices2;
print vertices;
"""


def test_example_belongs():
    assert check_parser_correct(example1)


def test_to_dot():
    res = generate_dot_str(example1)
    print(dedent(res))
    assert dedent(res) == dedent(
        """digraph tree {
1 [label=program];
1 -> 2;
2 [label=stmt];
2 -> 3;
3 [label=bind];
3 -> 4;
4 [label="TERM: let"];
3 -> 5;
5 [label=pattern];
5 -> 6;
6 [label=var];
6 -> 7;
7 [label="TERM: g1"];
3 -> 8;
8 [label="TERM: ="];
3 -> 9;
9 [label=expr];
9 -> 10;
10 [label="TERM: load"];
9 -> 11;
11 [label=stringLiteral];
11 -> 12;
12 [label="TERM: \\"wine.dot\\""];
1 -> 13;
13 [label="TERM: ;"];
1 -> 14;
14 [label=stmt];
14 -> 15;
15 [label=bind];
15 -> 16;
16 [label="TERM: let"];
15 -> 17;
17 [label=pattern];
17 -> 18;
18 [label=var];
18 -> 19;
19 [label="TERM: g"];
15 -> 20;
20 [label="TERM: ="];
15 -> 21;
21 [label=expr];
21 -> 22;
22 [label="TERM: set_start"];
21 -> 23;
23 [label=expr];
23 -> 24;
24 [label=val];
24 -> 25;
25 [label=setLiteral];
25 -> 26;
26 [label="TERM: {"];
25 -> 27;
27 [label=elem];
27 -> 28;
28 [label=intLiteral];
28 -> 29;
29 [label="TERM: 0"];
27 -> 30;
30 [label="TERM: .."];
27 -> 31;
31 [label=intLiteral];
31 -> 32;
32 [label="TERM: 100"];
25 -> 33;
33 [label="TERM: }"];
21 -> 34;
34 [label="TERM: of"];
21 -> 35;
35 [label=expr];
35 -> 36;
36 [label="TERM: ("];
35 -> 37;
37 [label=expr];
37 -> 38;
38 [label="TERM: set_final"];
37 -> 39;
39 [label=expr];
39 -> 40;
40 [label="TERM: ("];
39 -> 41;
41 [label=expr];
41 -> 42;
42 [label="TERM: get_vertices"];
41 -> 43;
43 [label=expr];
43 -> 44;
44 [label=var];
44 -> 45;
45 [label="TERM: g1"];
39 -> 46;
46 [label="TERM: )"];
37 -> 47;
47 [label="TERM: of"];
37 -> 48;
48 [label=expr];
48 -> 49;
49 [label=var];
49 -> 50;
50 [label="TERM: g1"];
35 -> 51;
51 [label="TERM: )"];
1 -> 52;
52 [label="TERM: ;"];
1 -> 53;
53 [label=stmt];
53 -> 54;
54 [label=bind];
54 -> 55;
55 [label="TERM: let"];
54 -> 56;
56 [label=pattern];
56 -> 57;
57 [label=var];
57 -> 58;
58 [label="TERM: l1"];
54 -> 59;
59 [label="TERM: ="];
54 -> 60;
60 [label=expr];
60 -> 61;
61 [label=expr];
61 -> 62;
62 [label=val];
62 -> 63;
63 [label=stringLiteral];
63 -> 64;
64 [label="TERM: \\"l1\\""];
60 -> 65;
65 [label="TERM: |"];
60 -> 66;
66 [label=expr];
66 -> 67;
67 [label=val];
67 -> 68;
68 [label=stringLiteral];
68 -> 69;
69 [label="TERM: \\"l2\\""];
1 -> 70;
70 [label="TERM: ;"];
1 -> 71;
71 [label=stmt];
71 -> 72;
72 [label=bind];
72 -> 73;
73 [label="TERM: let"];
72 -> 74;
74 [label=pattern];
74 -> 75;
75 [label=var];
75 -> 76;
76 [label="TERM: q1"];
72 -> 77;
77 [label="TERM: ="];
72 -> 78;
78 [label=expr];
78 -> 79;
79 [label=expr];
79 -> 80;
80 [label="TERM: ("];
79 -> 81;
81 [label=expr];
81 -> 82;
82 [label=expr];
82 -> 83;
83 [label=val];
83 -> 84;
84 [label=stringLiteral];
84 -> 85;
85 [label="TERM: \\"type\\""];
81 -> 86;
86 [label="TERM: |"];
81 -> 87;
87 [label=expr];
87 -> 88;
88 [label=var];
88 -> 89;
89 [label="TERM: l1"];
79 -> 90;
90 [label="TERM: )"];
78 -> 91;
91 [label="TERM: *"];
1 -> 92;
92 [label="TERM: ;"];
1 -> 93;
93 [label=stmt];
93 -> 94;
94 [label=bind];
94 -> 95;
95 [label="TERM: let"];
94 -> 96;
96 [label=pattern];
96 -> 97;
97 [label=var];
97 -> 98;
98 [label="TERM: q2"];
94 -> 99;
99 [label="TERM: ="];
94 -> 100;
100 [label=expr];
100 -> 101;
101 [label=expr];
101 -> 102;
102 [label=val];
102 -> 103;
103 [label=stringLiteral];
103 -> 104;
104 [label="TERM: \\"sub_class_of\\""];
100 -> 105;
105 [label="TERM: +"];
100 -> 106;
106 [label=expr];
106 -> 107;
107 [label=var];
107 -> 108;
108 [label="TERM: l1"];
1 -> 109;
109 [label="TERM: ;"];
1 -> 110;
110 [label=stmt];
110 -> 111;
111 [label=bind];
111 -> 112;
112 [label="TERM: let"];
111 -> 113;
113 [label=pattern];
113 -> 114;
114 [label=var];
114 -> 115;
115 [label="TERM: res1"];
111 -> 116;
116 [label="TERM: ="];
111 -> 117;
117 [label=expr];
117 -> 118;
118 [label=expr];
118 -> 119;
119 [label=var];
119 -> 120;
120 [label="TERM: g"];
117 -> 121;
121 [label="TERM: &"];
117 -> 122;
122 [label=expr];
122 -> 123;
123 [label=var];
123 -> 124;
124 [label="TERM: q1"];
1 -> 125;
125 [label="TERM: ;"];
1 -> 126;
126 [label=stmt];
126 -> 127;
127 [label=bind];
127 -> 128;
128 [label="TERM: let"];
127 -> 129;
129 [label=pattern];
129 -> 130;
130 [label=var];
130 -> 131;
131 [label="TERM: res2"];
127 -> 132;
132 [label="TERM: ="];
127 -> 133;
133 [label=expr];
133 -> 134;
134 [label=expr];
134 -> 135;
135 [label=var];
135 -> 136;
136 [label="TERM: g"];
133 -> 137;
137 [label="TERM: &"];
133 -> 138;
138 [label=expr];
138 -> 139;
139 [label=var];
139 -> 140;
140 [label="TERM: q2"];
1 -> 141;
141 [label="TERM: ;"];
1 -> 142;
142 [label=stmt];
142 -> 143;
143 [label=print];
143 -> 144;
144 [label="TERM: print"];
143 -> 145;
145 [label=expr];
145 -> 146;
146 [label=var];
146 -> 147;
147 [label="TERM: res1"];
1 -> 148;
148 [label="TERM: ;"];
1 -> 149;
149 [label=stmt];
149 -> 150;
150 [label=bind];
150 -> 151;
151 [label="TERM: let"];
150 -> 152;
152 [label=pattern];
152 -> 153;
153 [label=var];
153 -> 154;
154 [label="TERM: s"];
150 -> 155;
155 [label="TERM: ="];
150 -> 156;
156 [label=expr];
156 -> 157;
157 [label="TERM: get_start"];
156 -> 158;
158 [label=expr];
158 -> 159;
159 [label=var];
159 -> 160;
160 [label="TERM: g"];
1 -> 161;
161 [label="TERM: ;"];
1 -> 162;
162 [label=stmt];
162 -> 163;
163 [label=bind];
163 -> 164;
164 [label="TERM: let"];
163 -> 165;
165 [label=pattern];
165 -> 166;
166 [label=var];
166 -> 167;
167 [label="TERM: vertices1"];
163 -> 168;
168 [label="TERM: ="];
163 -> 169;
169 [label=expr];
169 -> 170;
170 [label="TERM: filter"];
169 -> 171;
171 [label=expr];
171 -> 172;
172 [label="TERM: ("];
171 -> 173;
173 [label=expr];
173 -> 174;
174 [label="TERM: map"];
173 -> 175;
175 [label=expr];
175 -> 176;
176 [label="TERM: ("];
175 -> 177;
177 [label=expr];
177 -> 178;
178 [label="TERM: get_edges"];
177 -> 179;
179 [label=expr];
179 -> 180;
180 [label=var];
180 -> 181;
181 [label="TERM: res1"];
175 -> 182;
182 [label="TERM: )"];
173 -> 183;
183 [label="TERM: with"];
173 -> 184;
184 [label=lambda];
184 -> 185;
185 [label=pattern];
185 -> 186;
186 [label="TERM: ("];
185 -> 187;
187 [label=pattern];
187 -> 188;
188 [label="TERM: ("];
187 -> 189;
189 [label=pattern];
189 -> 190;
190 [label=var];
190 -> 191;
191 [label="TERM: u_g"];
187 -> 192;
192 [label="TERM: ,"];
187 -> 193;
193 [label=pattern];
193 -> 194;
194 [label=var];
194 -> 195;
195 [label="TERM: u_q1"];
187 -> 196;
196 [label="TERM: )"];
185 -> 197;
197 [label="TERM: ,"];
185 -> 198;
198 [label=pattern];
198 -> 199;
199 [label=var];
199 -> 200;
200 [label="TERM: l"];
185 -> 201;
201 [label="TERM: ,"];
185 -> 202;
202 [label=pattern];
202 -> 203;
203 [label="TERM: ("];
202 -> 204;
204 [label=pattern];
204 -> 205;
205 [label=var];
205 -> 206;
206 [label="TERM: v_g"];
202 -> 207;
207 [label="TERM: ,"];
202 -> 208;
208 [label=pattern];
208 -> 209;
209 [label=var];
209 -> 210;
210 [label="TERM: v_q1"];
202 -> 211;
211 [label="TERM: )"];
185 -> 212;
212 [label="TERM: )"];
184 -> 213;
213 [label="TERM: =>"];
184 -> 214;
214 [label=expr];
214 -> 215;
215 [label=var];
215 -> 216;
216 [label="TERM: u_g"];
171 -> 217;
217 [label="TERM: )"];
169 -> 218;
218 [label="TERM: with"];
169 -> 219;
219 [label=lambda];
219 -> 220;
220 [label=pattern];
220 -> 221;
221 [label=var];
221 -> 222;
222 [label="TERM: v"];
219 -> 223;
223 [label="TERM: =>"];
219 -> 224;
224 [label=expr];
224 -> 225;
225 [label=expr];
225 -> 226;
226 [label=var];
226 -> 227;
227 [label="TERM: v"];
224 -> 228;
228 [label="TERM: in"];
224 -> 229;
229 [label=expr];
229 -> 230;
230 [label=var];
230 -> 231;
231 [label="TERM: s"];
1 -> 232;
232 [label="TERM: ;"];
1 -> 233;
233 [label=stmt];
233 -> 234;
234 [label=bind];
234 -> 235;
235 [label="TERM: let"];
234 -> 236;
236 [label=pattern];
236 -> 237;
237 [label=var];
237 -> 238;
238 [label="TERM: vertices2"];
234 -> 239;
239 [label="TERM: ="];
234 -> 240;
240 [label=expr];
240 -> 241;
241 [label="TERM: filter"];
240 -> 242;
242 [label=expr];
242 -> 243;
243 [label="TERM: ("];
242 -> 244;
244 [label=expr];
244 -> 245;
245 [label="TERM: map"];
244 -> 246;
246 [label=expr];
246 -> 247;
247 [label="TERM: ("];
246 -> 248;
248 [label=expr];
248 -> 249;
249 [label="TERM: get_edges"];
248 -> 250;
250 [label=expr];
250 -> 251;
251 [label=var];
251 -> 252;
252 [label="TERM: res2"];
246 -> 253;
253 [label="TERM: )"];
244 -> 254;
254 [label="TERM: with"];
244 -> 255;
255 [label=lambda];
255 -> 256;
256 [label=pattern];
256 -> 257;
257 [label="TERM: ("];
256 -> 258;
258 [label=pattern];
258 -> 259;
259 [label="TERM: ("];
258 -> 260;
260 [label=pattern];
260 -> 261;
261 [label=var];
261 -> 262;
262 [label="TERM: u_g"];
258 -> 263;
263 [label="TERM: ,"];
258 -> 264;
264 [label=pattern];
264 -> 265;
265 [label=var];
265 -> 266;
266 [label="TERM: u_q2"];
258 -> 267;
267 [label="TERM: )"];
256 -> 268;
268 [label="TERM: ,"];
256 -> 269;
269 [label=pattern];
269 -> 270;
270 [label=var];
270 -> 271;
271 [label="TERM: l"];
256 -> 272;
272 [label="TERM: ,"];
256 -> 273;
273 [label=pattern];
273 -> 274;
274 [label="TERM: ("];
273 -> 275;
275 [label=pattern];
275 -> 276;
276 [label=var];
276 -> 277;
277 [label="TERM: v_g"];
273 -> 278;
278 [label="TERM: ,"];
273 -> 279;
279 [label=pattern];
279 -> 280;
280 [label=var];
280 -> 281;
281 [label="TERM: v_q2"];
273 -> 282;
282 [label="TERM: )"];
256 -> 283;
283 [label="TERM: )"];
255 -> 284;
284 [label="TERM: =>"];
255 -> 285;
285 [label=expr];
285 -> 286;
286 [label=var];
286 -> 287;
287 [label="TERM: u_g"];
242 -> 288;
288 [label="TERM: )"];
240 -> 289;
289 [label="TERM: with"];
240 -> 290;
290 [label=lambda];
290 -> 291;
291 [label="TERM: ("];
290 -> 292;
292 [label=lambda];
292 -> 293;
293 [label=pattern];
293 -> 294;
294 [label=var];
294 -> 295;
295 [label="TERM: v"];
292 -> 296;
296 [label="TERM: =>"];
292 -> 297;
297 [label=expr];
297 -> 298;
298 [label=expr];
298 -> 299;
299 [label=var];
299 -> 300;
300 [label="TERM: v"];
297 -> 301;
301 [label="TERM: in"];
297 -> 302;
302 [label=expr];
302 -> 303;
303 [label=var];
303 -> 304;
304 [label="TERM: s"];
290 -> 305;
305 [label="TERM: )"];
1 -> 306;
306 [label="TERM: ;"];
1 -> 307;
307 [label=stmt];
307 -> 308;
308 [label=bind];
308 -> 309;
309 [label="TERM: let"];
308 -> 310;
310 [label=pattern];
310 -> 311;
311 [label=var];
311 -> 312;
312 [label="TERM: vertices"];
308 -> 313;
313 [label="TERM: ="];
308 -> 314;
314 [label=expr];
314 -> 315;
315 [label=expr];
315 -> 316;
316 [label=var];
316 -> 317;
317 [label="TERM: vertices1"];
314 -> 318;
318 [label="TERM: &"];
314 -> 319;
319 [label=expr];
319 -> 320;
320 [label=var];
320 -> 321;
321 [label="TERM: vertices2"];
1 -> 322;
322 [label="TERM: ;"];
1 -> 323;
323 [label=stmt];
323 -> 324;
324 [label=print];
324 -> 325;
325 [label="TERM: print"];
324 -> 326;
326 [label=expr];
326 -> 327;
327 [label=var];
327 -> 328;
328 [label="TERM: vertices"];
1 -> 329;
329 [label="TERM: ;"];
1 -> 330;
330 [label="TERM: <EOF>"];
}
"""
)
