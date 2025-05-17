%------------------------------------------------------------------------------
% Prolog Family and Muslim Marriage Knowledge Base (with Age)
%
% This file defines family relationships and rules for marriage validity
% specifically within the Muslim community, incorporating age checks.
% Non-Muslim individuals and Ahli Kitab marriage are excluded.
%
% Facts:
% - male(Person), female(Person): Gender.
% - parent(Parent, Child): Biological parent-child link.
% - spouse(Person1, Person2): Indicates a valid existing marriage (symmetric).
% - is_muslim(Person): Person is Muslim (all individuals in this KB are Muslim).
% - birth_year(Person, Year): The birth year of a person.
% - current_year(Year): The current year (USER NEEDS TO UPDATE THIS FACT).
%
% Rules:
% - Derived family relationships (father, mother, sibling, etc.).
% - age(Person, Age): Calculates the age of a person based on birth year and current year.
% - is_adult(Person): Checks if a person is 18 years or older (example definition of adult).
% - is_marriageable_age(Person): Checks if a person meets a minimum age for marriage (e.g., 18 in this example, acknowledging jurisprudential nuances).
% - is_mahram(Person1, Person2): Permanent marriage prohibition (kinship/affinity).
% - count_wives(Husband, Count): Counts existing wives.
% - valid_islamic_marriage(Husband, Wife): Checks if a proposed marriage is valid
%   based on gender, Muslim status, not being Mahram, polygyny limit, AND AGE.
%
% Boundaries for Marriage Rules:
% - Community: Applies only to marriages between Muslims.
% - Gender: Male (Husband) and female (Wife).
% - Religion: Both Muslim.
% - Prohibited Relations (Mahram): Must not be Mahram.
% - Polygyny: Man <= 4 wives. Woman <= 1 husband (implicit).
% - Age: Both must meet `is_marriageable_age` criteria (e.g., >= 18). This is a legal/social boundary added to the religious one.
% - Procedural/Legal: Consent, witnesses, mahr, wali are assumed handled externally.
% - Fosterage: Acknowledged but not modeled.
%------------------------------------------------------------------------------

%------------------------------------------------------------------------------
% Section 1: Basic Facts about Individuals and Direct Relationships (Muslims Only)
%------------------------------------------------------------------------------

% --- Gender Facts ---
male(tahir).
male(umair).
male(altaf).
male(khadam).

female(saman).
female(zainab).
female(maria).
female(noreena).
female(razia).
female(asia).

% --- Parent Facts (Parent, Child) ---
parent(tahir, zainab).
parent(tahir, umair).
parent(tahir, maria).
parent(saman, zainab).
parent(saman, umair).
parent(saman, maria).
parent(altaf, saman).
parent(noreena, saman).
parent(khadam, tahir).
parent(razia, tahir).
parent(altaf, asia).
parent(noreena, asia).

% --- Spouse Facts (assert symmetrically spouse(A, B) and spouse(B, A)) ---
spouse(tahir, saman).
spouse(saman, tahir).
spouse(altaf, noreena).
spouse(noreena, altaf).
spouse(khadam, razia).
spouse(razia, khadam).

% --- Friend Facts (symmetric) ---
friend(umair, ibrahim).
friend(umair, irtaza).
friend(umair, zohaib).

% --- Best-Friend Facts (directional) ---
best_friend(umair, hassan).
best_friend(umair, dawood).

% --- Religious Affiliation Facts (All individuals in this KB are Muslim) ---
is_muslim(tahir).
is_muslim(saman).
is_muslim(umair).
is_muslim(zainab).
is_muslim(maria).
is_muslim(khadam).
is_muslim(altaf).
is_muslim(razia).
is_muslim(noreena).

% --- Birth Year Facts ---
% Add realistic or illustrative birth years for individuals.
birth_year(tahir, 1975).
birth_year(saman, 1978).
birth_year(umair, 2005). % Example: Younger
birth_year(zainab, 2002). % Example: Potentially Marriageable Age
birth_year(maria, 2010). % Example: Child
birth_year(khadam, 1950).
birth_year(altaf, 1955).
birth_year(razia, 1952).
birth_year(noreena, 1958).

% --- Current Year Fact (!!! USER NEEDS TO UPDATE THIS !!!) ---
% Change this fact to the current year when using the KB.
current_year(2020).


%------------------------------------------------------------------------------
% Section 2: Rules for Derived Family Relationships (and Age)
%------------------------------------------------------------------------------

% --- Basic Parent/Child Variations ---

father(F, C) :- parent(F, C), male(F).
mother(M, C) :- parent(M, C), female(M).
child(C, P) :- parent(P, C).
son(S, P) :- child(S, P), male(S).
daughter(D, P) :- child(D, P), female(D).

% --- Grandparent/Grandchild Variations ---

grandparent(GP, GC) :- parent(GP, P), parent(P, GC).

% Maternal grandparents
maternal_grandfather(MGF, GC) :- mother(M, GC), father(MGF, M).
maternal_grandmother(MGM, GC) :- mother(M, GC), mother(MGM, M).

% Paternal grandparents
paternal_grandfather(PGF, GC) :- father(F, GC), father(PGF, F).
paternal_grandmother(PGM, GC) :- father(F, GC), mother(PGM, F).

grandchild(GC, GP) :- grandparent(GP, GC).
grandson(GS, GP) :- grandchild(GS, GP), male(GS).
granddaughter(GD, GP) :- grandchild(GD, GP), female(GD).

% --- Sibling Variations ---

sibling(S1, S2) :- parent(P, S1), parent(P, S2), S1 \== S2.
brother(B, S) :- sibling(B, S), male(B).
sister(S, Sibling) :- sibling(S, Sibling), female(S).

% --- Aunt/Uncle/Nephew/Niece ---

% -- Maternal uncles and aunts --
maternal_uncle(U, C) :- mother(M, C), brother(U, M), male(U).
maternal_aunt(A, C) :- mother(M, C), sister(A, M), female(A).

% -- Paternal uncles and aunts --
paternal_uncle(U, C) :- father(F, C), sibling(U, F), male(U).
paternal_aunt(A, C) :- father(F, C), sibling(A, F), female(A).

nephew(Nephew, UncleOrAunt) :- parent(P, Nephew), sibling(UncleOrAunt, P), male(Nephew).
niece(Niece, UncleOrAunt) :- parent(P, Niece), sibling(UncleOrAunt, P), female(Niece).

% --- Cousin ---

cousin(C1, C2) :- parent(P1, C1), parent(P2, C2), sibling(P1, P2), C1 \== C2.

% --- Friend Rule (ensures symmetry) ---
friends(X,Y) :- friend(X,Y).
friends(X,Y) :- friend(Y,X).

% --- Best-Friend Rule (one-way or mutual if declared both ways) ---
best_friend_of(X,Y) :- best_friend(X,Y).

% you can also write a mutual best-friend predicate if you like:
mutual_best_friends(X,Y) :-
    best_friend(X,Y),
    best_friend(Y,X).


% --- Ancestor/Descendant (Transitive Relationships) ---

ancestor(A, D) :- parent(A, D).
ancestor(A, D) :- parent(A, P), ancestor(P, D).
descendant(D, A) :- ancestor(A, D).

% --- Spouse Variations ---

husband(H, W) :- spouse(H, W), male(H), female(W).
wife(W, H) :- spouse(W, H), female(W), male(H).

% --- Age Calculation ---

% age(Person, Age): Calculates the age of a Person.
age(Person, Age) :-
    birth_year(Person, BirthYear),
    current_year(CurrentYear),
    Age is CurrentYear - BirthYear.

% --- Age-based Status ---

% is_adult(Person): A person is considered an adult if 18 or older.
is_adult(Person) :-
    age(Person, Age),
    Age >= 18.

% is_minor(Person): A person is considered a minor if younger than 18.
is_minor(Person) :-
    age(Person, Age),
    Age < 18.

% --- Marriageable Age ---
% Defines the minimum age for marriage. Using 18 as an example threshold.
% In Islamic jurisprudence, this is often linked to puberty, but many
% jurisdictions combine this with a minimum legal age like 16 or 18.
% This rule uses a simple fixed age for the KB.

is_marriageable_age(Person) :-
    age(Person, Age),
    Age >= 18. % Example threshold: 18 years or older


%------------------------------------------------------------------------------
% Section 3: Rules for Muslim Marriage Validity and Prohibitions (with Age)
%------------------------------------------------------------------------------

% is_mahram(Person1, Person2)
% Person1 and Person2 are Mahram, meaning they are permanently prohibited
% from marrying each other in Islam due to kinship or affinity.

is_mahram(P1, P2) :-
    P1 \== P2, % Cannot be Mahram to self
    (   is_mahram_kinship(P1, P2)
    ;   is_mahram_affinity(P1, P2)
        % ; is_mahram_fosterage(P1, P2) % Add rules here if modeling fosterage
    ).

% --- Mahram by Kinship (Blood Relation) ---
% Prohibitions stemming from biological relationships.

is_mahram_kinship(P1, P2) :- ancestor(A, P1), descendant(A, P2).
is_mahram_kinship(P1, P2) :- ancestor(A, P2), descendant(A, P1).

is_mahram_kinship(P1, P2) :- sibling(P1, P2).

is_mahram_kinship(P1, P2) :- sibling(S, P1), descendant(S, P2).
is_mahram_kinship(P1, P2) :- sibling(S, P2), descendant(S, P1).

is_mahram_kinship(P1, P2) :- parent(P, P1), sibling(S, P), S = P2.
is_mahram_kinship(P1, P2) :- parent(P, P2), sibling(S, P), S = P1.

% --- Mahram by Affinity (Relation by Marriage) ---
% Prohibitions stemming from valid marriage relationships.

is_mahram_affinity(P1, P2) :- spouse(P1, S), parent(P2, S).
is_mahram_affinity(P1, P2) :- spouse(P2, S), parent(P1, S).

is_mahram_affinity(P1, P2) :- spouse(P1, S), parent(S, P2).
is_mahram_affinity(P1, P2) :- spouse(P2, S), parent(S, P1).

is_mahram_affinity(P1, P2) :- ancestor(A, P1), spouse(P2, A).
is_mahram_affinity(P1, P2) :- ancestor(A, P2), spouse(P1, A).

is_mahram_affinity(P1, P2) :- descendant(D, P1), spouse(D, P2).
is_mahram_affinity(P1, P2) :- descendant(D, P2), spouse(D, P1).


% --- Mahram by Fosterage ---
% (Requires specific facts and rules about nursing relationships, age, etc.)
% Not implemented here.

% --- Rule for Counting Wives ---
% Counts the number of existing spouses for a Muslim male.

count_wives(Husband, Count) :-
    male(Husband),
    is_muslim(Husband),
    findall(Wife, (spouse(Husband, Wife), female(Wife)), WivesList),
    length(WivesList, Count).


% --- Rule for Valid Islamic Marriage (Within Muslim Community, with Age Check) ---
% Checks if a proposed marriage is permitted based on all criteria.

valid_islamic_marriage(Husband, Wife) :-
    male(Husband),
    female(Wife),
    is_muslim(Husband),
    is_muslim(Wife),
    not(is_mahram(Husband, Wife)),
    count_wives(Husband, CurrentWives),
    CurrentWives < 4,
    is_marriageable_age(Husband), % Both must meet the age requirement
    is_marriageable_age(Wife).


%------------------------------------------------------------------------------
% Section 4: Example Queries (for testing in a Prolog interpreter)
%------------------------------------------------------------------------------

% Load the KB: consult('family_muslim_marriage_with_age_kb.pl').
% !!! REMEMBER TO UPDATE the current_year(YYYY). fact !!!

% --- Testing Basic Family Relations ---
% ?- father(tahir, zainab).       % true
% ?- sibling(zainab, umair).      % true
% ?- uncle(altaf, zainab).        % true (Altaf is Saman's spouse, Saman is parent of Zainab. My uncle rule is sibling of parent. Let's re-check uncle rule.)
% -> uncle(U, N) :- sibling(U, P), parent(P, N), male(U).
% -> Is Altaf a sibling of Saman? No (Altaf is spouse of Noreena, Saman is daughter of Altaf/Noreena).
% -> Is Altaf a sibling of Tahir? No.
% My uncle rule is correct for biological uncles (parent's brother). It doesn't cover uncle-by-marriage (aunt's husband).
% If you want to model Uncles/Aunts by marriage, you need separate rules like:
% uncle_by_marriage(U, N) :- aunt(A, N), spouse(U, A), male(U).
% aunt_by_marriage(A, N) :- uncle(U, N), spouse(A, U), female(A).
% The current `uncle` rule is for biological uncles, which is the standard definition in such KBs and for Mahram.

% Let's check the actual uncle/aunt in the facts:
% Tahir's siblings? None listed (only parents Khadam/Razia).
% Saman's siblings? None listed (only parents Altaf/Noreena).
% So, Tahir and Saman have no biological siblings in this KB. Thus, their children (Zainab, Umair, Maria) have no biological aunts/uncles in this KB.
% Queries like ?- uncle(U, zainab). should fail.
% Queries like ?- aunt(A, umair). should fail.
% Queries like ?- is_mahram(altaf, zainab). % Altaf is grandfather of Zainab. ancestor(altaf, zainab). True.

% --- Testing Age ---
% ?- age(tahir, Age).           % Age = 2024 - 1975 = 49. true.
% ?- age(umair, Age).           % Age = 2024 - 2005 = 19. true.
% ?- age(maria, Age).           % Age = 2024 - 2010 = 14. true.

% --- Testing Age-based Status ---
% ?- is_adult(tahir).          % age 49 >= 18. true.
% ?- is_adult(umair).           % age 19 >= 18. true.
% ?- is_adult(maria).           % age 14 < 18. false.
% ?- is_minor(maria).           % age 14 < 18. true.
% ?- is_marriageable_age(zainab). % age 2024 - 2002 = 22. 22 >= 18. true.
% ?- is_marriageable_age(umair).  % age 19 >= 18. true.
% ?- is_marriageable_age(maria).  % age 14 < 18. false.

% --- Testing Mahram ---
% ?- is_mahram(tahir, saman).     % Married couple. false.
% ?- is_mahram(tahir, zainab).    % Parent/Child. true.
% ?- is_mahram(zainab, umair).    % Siblings. true.
% ?- is_mahram(altaf, zainab).    % Grandparent/Grandchild. true.
% ?- is_mahram(altaf, tahir).     % Father-in-law/Son-in-law (Saman's father, Tahir is Saman's spouse). parent(altaf, saman), spouse(tahir, saman). true.
% ?- is_mahram(tahir, noreena).   % Mother-in-law/Son-in-law (Saman's mother, Tahir is Saman's spouse). parent(noreena, saman), spouse(tahir, saman). true.

% --- Testing Polygyny Count ---
% Tahir has Saman (1 wife).
% ?- count_wives(tahir, N).      % N = 1.
% Khadam has Razia (1 wife).
% ?- count_wives(khadam, N).     % N = 1.
% Altaf has Noreena (1 wife).
% ?- count_wives(altaf, N).      % N = 1.

% --- Testing Valid Islamic Marriage (with Age Check) ---
% Valid cases (assuming both are Muslims, not Mahram, and meet age >= 18):
% Tahir (49), Saman (46) - Married. Validatable by rule.
% ?- valid_islamic_marriage(tahir, saman). % male(tahir), female(saman), is_muslim(tahir), is_muslim(saman), not(is_mahram(tahir, saman)), count_wives(tahir, 1) < 4, is_marriageable_age(tahir), is_marriageable_age(saman). All true. true.

% Potential new marriages (check age and Mahram):
% Zainab (22), Umair (19) - Siblings -> Mahram.
% ?- valid_islamic_marriage(umair, zainab). % Mahram. false.
% Zainab (22), Maria (14) - Siblings -> Mahram. Maria is minor.
% ?- valid_islamic_marriage(umair, maria). % Mahram AND Maria is too young. false.
% Maria (14), Umair (19) - Invalid Gender AND Maria is too young.
% ?- valid_islamic_marriage(maria, umair). % Invalid Gender. false.

% Consider marriage between Umair (19) and a potential new person, 'amina' (female, muslim, born 2003, age 21).
% Add facts: female(amina). is_muslim(amina). birth_year(amina, 2003).
% Check if Umair and Amina are Mahram (they are not based on current KB).
% Check Umair's wives (0). 0 < 4.
% Check ages: Umair 19 (>=18), Amina 21 (>=18).
% ?- valid_islamic_marriage(umair, amina). % Will be true if amina facts are added.

% Invalid Age example:
% ?- valid_islamic_marriage(tahir, maria). % Tahir(M,M), Maria(F,M), Not Mahram, Tahir < 4 wives. BUT Maria's age is 14 (<18). false.
% ?- valid_islamic_marriage(umair, maria). % Umair(M,M), Maria(F,M), Mahram (siblings) AND Maria's age < 18. false.

% Finding potential spouses:
% ?- valid_islamic_marriage(umair, X). % Find valid Muslim wives for Umair (Muslim, not Mahram, age >= 18, Umair age >= 18, Umair has 0 wives).
% This query will check all female, Muslim individuals >= 18 in the KB who are not Mahram to Umair.
% In this KB, only Zainab and Maria are Umair's siblings (Mahram). Saman and Razia are too old (mothers'/grandmothers' generation). Noreena is Altaf's wife (Altaf is Saman's parent, Saman is Umair's parent. Noreena is Umair's grandmother. Mahram).
% The query `?- valid_islamic_marriage(umair, X).` should return false, as there are no valid *new* spouses for Umair based *only* on the individuals defined with birth years in the current KB.

% To find all valid marriage pairs in the KB:
% ?- valid_islamic_marriage(Husband, Wife).

% To find valid *new* marriage pairs:
% ?- valid_islamic_marriage(Husband, Wife), \+ spouse(Husband, Wife).