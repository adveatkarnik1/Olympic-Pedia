import os
from langchain import FewShotPromptTemplate
from langchain import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import gradio as gr
from langchain.agents import create_csv_agent
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain.agents import initialize_agent
from langchain.utilities import WikipediaAPIWrapper


from system import openaiapikey
os.environ['OPENAI_API_KEY']=openaiapikey
chat = ChatOpenAI(model='gpt-3.5-turbo',temperature=0)

examples = [
  {
    "question": "My height is 1.95 m and weight is 94 kg , for running in the olympics in 3 months, make me a custom exercise plan with specific exercises and number of sets, which is specified for my height and weight.",
    "answer":
"""
GYM Workouts:

Leg Raises (sets: 3, rest: 30secs)

Side Sweeps (3 sets with 30secs rest)

Reverse Crunches (sets: 3, rest: 30secs)

Side Plank Clams (3 sets with 30secs rest)

Bunny Hops (sets: 5, reps: 20)

Box Jumps (sets: 4, reps: 8)

Bounding (sets: 3, reps: 10)

Cable Knee Drives (sets: 3, reps: 10)

Hanging Leg Raises (sets: 3, reps: 10)

Workout 1:

Box Jump with Medicine Ball Slam (sets: 4, reps: 5)

Good Morning (sets: 4, reps: 8)

Barbell Lunge (sets: 3, reps: 10)

Sled Push (sets: 3, reps: 20)

Barbell Landmine Exercises (sets: 3, reps: 20)

Workout 2:

Power Clean (sets: 5, reps: 3)

Explosive Barbell Step-Ups (sets: 4, reps: 6-8)

Romanian Deadlift (sets: 4, reps: 10)

Sled Drag (sets: 3, reps: 20)

Barbell Ab Rollout (sets: 3, reps: 10)

On the track:

To train for 100m-200m sprint races, Usain Bolt divides the speed into five phases involving the following drills:

Starting Blocks: Example workout: 10×2 point start for 10-20 m (rest: 2mins), 6×3 point start for 10-20 m (rest: 3mins), 4×2 block starts for 10-30 m (rest: 5mins)

Acceleration: Example Workout: 10×20 m with weight vest (4mins recovery), 5×15 m 2-point start using weight sleds (5mins recovery)

Top End Speed: Example Workout: 5×30 m acceleration, 75 percent speed for 15-20 m, sprint for 10-15 m (rest: 4-5mins)

Deceleration: Example Workout: 2×100 m (2-3 reps), 95 percent of 200m pace (rest: 2-3mins between reps, 5-8mins between sets)

Speed Endurance: Example Workout: 6-8x150m, 80-90% of 200m pace (rest: 3-4mins)

Diet:

5.000 calories a day, calibrating each of your six meals with 60% protein, 30% carbohydrates and 10% fat. Drink plenty of water.

Breakfast- dumplings of flour, water, butter and milk and boiled potatoes

Lunch-fish, accompanied by a portion of rice or pasta and one of whole wheat bread and plenty of vegetables

Dinner-bananas, mangoes, pineapples and apples
"""
  },

{
  "question":"My height is 1.8 m and weight is 80 kg , for running in the olympics in 3 months, make me a custom exercise plan with specific exercises and number of sets, which is specified for my height and weight.",
  "answer": '''

  Warmup Exercise:

  Crab Walks. 10-15 Steps Each Side (3 Sets)
Glute KickBacks. 10-15 Reps Each Leg (3 Sets)
Knee Turns into Band. 10-15 Each Leg (3 Sets)
Side-Lying Clams. 10-15 Each Leg (3 Sets)
Resisted Knee Drives. 10-15 Each Leg (3 Sets)

  lower body workouts consisting of sets/reps of 3x15. Some of the exercises he incorporates are squats and plyometrics. Training 60 hours per week

  Diet:
  6000 calories per day.230 grams of protein daily, 308 grams of carbohydrates, maybe 70 grams of fat
  Food to consider eating- Tuna fish, lean beef, lean beef, lean pork, ground turkey, fish, lean steak, soy milk, Greek yogurt, brown rice, raisins, six egg whites, two whole eggs, 45 grams of oatmeal'''
},
{"question": "My height is 1.93 m and weight is 88 kg , for swimming in the olympics in 3 months, make me a custom exercise plan with specific exercises and number of sets, which is specified for my height and weight.",
    "answer": '''
    Swimming routine:
1. Sidekick (6 sets, 50 reps)
2. Butterfly swimming drills (6 sets, 50 reps)
3. Pull buoy (6 sets, 50 reps)
4. Fly (25 reps)
5. Free (50 reps)
6. Fly (50 reps)
7. Strokes (500 reps)
8. Kick (50 reps)
9. Free (50 reps)
10. 2000 timed kick stroke
11. IM continuous drill (4 sets, 100 reps)
12. Ab exercises (500 reps)
 Gym routine:
1. Standing Dumbbell Press (3 sets, 10-16 reps)
2. Dumbbell Front Raise (3 sets, 10-16 reps)
3. Dumbbell Lateral Shoulder Raise (3 sets, 10-16 reps)
4. Compound movements (3 sets, 10-16 reps)

Diet:
1. Breakfast
• Fried-egg sandwiches
• Two cups of coffee
• One five-egg omelet
• One bowl of porridge
• French toast
• Three chocolate-chip pancakes
2. Lunch
• Half a kg of pasta
• Two large ham and cheese sandwiches
Energy drinks
3. Dinner
• Half a kg of pasta
• An entire pizza
• More energy drinks
Supplements:
• Creatine
• Vitamin C
• Protein Shakes
    '''},
{
      'question':"My height is 1.88 m and weight is 88 kg , for swimming in the olympics in 3 months, make me a custom exercise plan with specific exercises and number of sets, which is specified for my height and weight.",

      'answer':'''
      Odd days:
      3-4 sets of deadlifts of 10-12 reps
3-4 sets of farmer’s walks of 10-12 reps
3-4 sets of squats of 10-12 reps
3-4 sets of rope swings of 10 reps
3-4 sets of bent-over rows of 10 reps
Sessions of weight lifting during the day
Interval training in the pool
Repeats of 100-meter swims
Repeats of 200-meter swims
Repeats of 400-meter swims
3-4 sets of kettlebells of 8-10 reps
3-4 sets of cross-fit of 8-10 reps
3-4 sets of tire flips
3-4 sets of keg tosses of 10 reps
Lifting of metal logs in a session twice a week
5000-10000 strokes per 2 hours of workout
20 sets of sandbag squats
Even days:
4 sets of squats of 10-12 reps
5-6 sets of rope swings of 10 reps
5-6 sets of bent-over rows of 10 reps
5-6 sets of tire flips
5-6 sets of keg tosses of 10 reps
5-6 sets of kettlebells of 8-10 reps
3-4 sets of cross-fit of 8-10 reps
3-4 sets of deadlifts of 10-12 reps
5-6 sets of farmer’s walks of 10-12 reps
2-3 sets of bent-over rows of 12 reps
2-3 sets of chest press on the back along with a weight plate of 10-12 reps
30 sets of burpees

Diet:
BREAKFAST

6 eggs, scrambled — 597 calories

-with ham, 1 slice — 46 calories

-with spinach, 1 cup — 41 calories

-with diced tomatoes, 1/2 cup — 25 calories

Hash browns, 1 cup — 413 calories

Pancakes, plain, 2 — 298 calories

Oatmeal, plain, 1 cup — 166 calories

Fruit — 1 banana — 105 calories

Total: 1,691 calories

SNACK

Avocado toast:

-1/2 an avocado — 145 calories

-whole wheat bread slice — 69 calories

-with spinach, 5 leaves — 12 calories

-with an egg — 91 calories

-with hot sauce — 1 calorie

-with tofu sausage — 120 calories

Total: 438 calories

LUNCH

Fettuccine Alfredo — 950 calories

-with chicken — 282 calories

Water with lemon-flavored MiO drops — 0 calories

Total: 1,232 calories

SNACKS

Peanut Butter Kind bar, probably plus protein — 200 calories

Total: 200 calories

DINNER


Domino's Pizza, cheese, 3 slices — 870 calories

Domino's BBQ Wings, 4 — 960 calories

-with blue cheese — 240 calories

Mountain Dew, two 12-ounce servings — 340 calories

Total: 2,410 calories

DESSERT

Mint chocolate chip ice cream, 1 cup — 300 calories

Total: 300 calories

GRAND TOTAL: 6,271 calories
      '''
    },
    {
      "question":"My height is 1.82 m and weight is 72.5 kg , for playing tennis in the olympics in 3 months, make me a custom exercise plan with specific exercises and number of sets, which is specified for my height and weight.",
  "answer":'''

  Warmup: 20 minutes of everything from ellipticals to jogging steps and jump rope to sideline sprints or butt kicks
  Strength Workout: 5 sets of 15 reps of Medicine Ball Lunges, 5 sets of 60 second Medicine Ball Shuffle Steps,Chest flys: 3 sets of 15 reps,Chest flys: 3 sets of 15 reps,Lat pulldown: 3 sets of 15 reps
Cone Drills: 5 to 10 cones set up only a few feet apart, it’s all about zig-zagging between the cones forward and backward,5 sets of 90 seconds.
Racket Drills 20 minutes
HIIT training (5 exercises for 15 seconds, then 15 second rest):
Push-ups
Squats
Squat jumping jacks
Leg raises
Ab crunches
Jump rope
Lateral raises
Chin-ups

Diet:

Breakfast:
Fresh squeezed orange juice
Coffee
Waffles or pancakes with fruit compote
Tablespoon of apple cider vinegar

Snack:

Protein bars
Cup of unsalted nuts
Lunch:

Bowl of pasta with chicken strips
Fresh leafy green salad

Snack:
Bananas and fresh berries
Protein shake
Dinner:

Any kind of meat or fish main course
Large portion of green vegetables
Ice cream
  '''
    },
{ "question":"My height is 1.88 m and weight is 77 kg , for playing tennis in the olympics in 3 months, make me a custom exercise plan with specific exercises and number of sets, which is specified for my height and weight.",

  "answer":'''
 Inverted hamstring stretch
Squat thrusts
Jumping jacks
Reverse lunge with backward reach
Lunge with side bend
Walking high knees
Low side-to-side lunge
Walking high kicks
Inchworm

Foam rolling the following parts of body:
Calves
Glutes
Lower Back
Upper Back
Hamstring
Quads
Hips
Shoulder Blades

Do yoga

Breakfast:

Water first thing out of bed
Two tablespoons of honey
Muesli (including organic gluten-free rolled oats, cranberries, raisins, pumpkin or sunflower seeds, and almonds)
Banana with cashew butter
Gluten-free oats with cashew butter and bananas
Fruit
Mid-morning Snack (if needed):

Gluten-free bread or crackers with avocado and tuna
Gluten-free toast with almond butter and honey
Home-made hummus (including chickpeas and gluten-free soy sauce) with apples/crudités
Lunch:

Mixed-greens salad
Gluten-free pasta primavera (including rice pasta, summer squash, courgettes, asparagus, sun-dried tomatoes, and optional vegan cheese)
Spicy soba noodle salad (including gluten-free soba noodles, red bell pepper, rocket, cashews, and basil leaves, plus spicy vinaigrette)
Gluten-free pasta with power pesto (including rice pasta, walnuts, and basil leaves)
Tuna nicoise salad (green beans, cannellini beans, rocket, tuna, red pepper, tomatoes, and canned chickpeas)
Fresh mixed-greens salad with avocado and home-made dressing
Mid-afternoon Snack:

Apple with cashew butter; melon
Fruit and nut bar; fruit
Avocado with gluten-free crackers; fruit
Dinner:

Kale caesar salad (kale, fennel, quinoa, and pine nuts) plus dressing (including anchovies or sardines)
Minestrone soup
Salmon fillets (skin on) with roasted tomatoes and marinade
Tomato soup
Roasted tomatoes
Carrot and ginger soup
Whole lemon-roasted chicken
  '''
}

]

example_template = """
User: {question}
AI: {answer}
"""
example_prompt = PromptTemplate(
    input_variables=["question", "answer"],
    template=example_template
)


prefix = """ The assistant is a world class dietician and a gym trainer and  is typically informative and complete.
It gives complete diet and exercise plan for upcoming olympians.
It currently specialises in 3 sports - tennis, running and swimming.
The assisstant bases it diet on the diet of olympians who are the best in their respective fields.
 Here are some examplees of excerpts b/w user and the assiatant"""

suffix = """
User: {question}
AI: """

few_shot_prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=prefix,
    suffix=suffix,
    input_variables=["question"],
    example_separator="\n\n"
)

memory = ConversationBufferMemory(
    memory_key='chat_history',
    return_messages=True
)

chain = LLMChain(llm=chat, prompt=few_shot_prompt_template,verbose=True,memory=memory)


def ask(weight,height,sport,display):
    sport=sport.lower()
    if sport=='tennis':
        sport='playing tennis'
    
    # Store original input values
    original_height = height
    original_weight = weight

    # Process height input
    height = float(height)  # Convert to float
    if height < 3:
        # If height < 3, assume meters
        height_unit = 'm'
    elif 3 <= height <= 10:
        # If 3 <= height <= 10, assume feet and convert to m
        height = height * 0.3048
        height_unit = 'feet'
    else:
        # If height > 10, assume cm and convert to m
        height = height / 100
        height_unit = 'cm'
    
    # Round the height to 3 decimal places
    height = round(height, 3)
    
    # Process weight input
    weight = float(weight)  # Convert to float
    if weight > 200:
        # If weight > 200, assume pounds and convert to kg
        weight = weight / 2.2046
        weight_unit = 'pounds'
    else:
        # If weight <= 200, assume kg
        weight_unit = 'kg'

    # Round the weight to 3 decimal places
    weight = round(weight, 3)

    question=f"My height is {original_height} {height_unit} ({height} m) and weight is {original_weight} {weight_unit} ({weight} kg) , for {sport} in the olympics in 3 months, make me a custom exercise plan with specific exercises and number of sets, which is specified for my height and weight."
    display = display or []
    show = list(sum(display, ()))
    show.append(input)
    response=chain.predict(question=question)
    display.append((question, response))
    return display,display


#use .predict
block = gr.Blocks()
with block:
    gr.Markdown("""<h1><center>MY AI TRAINER</center></h1>
    """)
    chatbot = gr.Chatbot()
    weight = gr.Textbox(placeholder="In kg ",label="WEIGHT")
    height = gr.Textbox(placeholder="In m ",label="HEIGHT")
    sport = gr.Textbox(placeholder="Running, Tennis or Swimming?",label="SPORT")
    state = gr.State()
    submit = gr.Button("PLAN MY EXERCISE AND DIET")
    submit.click(ask, inputs=[weight,height,sport, state], outputs=[chatbot, state])

block.launch(debug = True)