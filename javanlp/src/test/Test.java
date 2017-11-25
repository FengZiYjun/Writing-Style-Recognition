package test;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import org.fnlp.nlp.cn.CNFactory;
import org.fnlp.nlp.parser.dep.DependencyTree;
import org.fnlp.util.exception.LoadModelException;

public class Test {

	// 30 dependency features
	public final static String[] depens = {"之字结构", "时态", "构式", "修饰", "话题", "关联",
			"同位", "数量", "顺承", "定语", "主语", "限定", "从属", "介宾", "标签", "连动",
			"总括", "标点", "的字结构", "Root" ,"宾语", "语态", "并列", "得字结构", "地字结构",
			"核心词", "疑问连动", "感叹", "补语", "状语"};
	
	private static String saveText = new String();
	
	
	public static String makeText(){
		return saveText;
	}
	
	
	public static HashMap<String, Integer> computeDepen(ArrayList<java.util.List<String>> result){
		HashMap<String, Integer> grammar_counter = new HashMap<String, Integer>();
		
		for(String item : depens){
			grammar_counter.put(item, 0);
		}
		List<String> tmp;
		String newText = new String();
		
		for(int i=0;i<result.size();i++){
			tmp = result.get(i);
			String grammar_tag = tmp.get(3);
			newText += Arrays.asList(depens).indexOf(grammar_tag) + " ";
			//System.out.println(tmp.toString());
			grammar_counter.put(grammar_tag, grammar_counter.get(grammar_tag) + 1);
			
		}
		saveText += newText + "\n";
		return grammar_counter;
	}
	
	
	public static HashMap<String, Integer> sentenceDep(String sentence) throws LoadModelException{
		
		CNFactory factory = CNFactory.getInstance("models");
		DependencyTree tree = factory.parse2T(sentence);
		ArrayList<java.util.List<String>> result = tree.toList();
		
		return computeDepen(result);
	}
	
	public static String[] split(String filenames){
		return filenames.split(",");
	}
	
	public static void run(String filename){
		final String PATH = "..\\src\\output\\";
		final String FILE = "cleaned_" + filename;
		System.out.println("dealing with " + FILE);
		
		String text = new String();
		HashMap<String, Integer> features = new HashMap<String, Integer>();
		for(String item : depens){
			features.put(item, 0);
		}
		File fileDirs = new File(PATH + FILE);
		
		try {
			//Scanner in = new Scanner(Paths.get(PATH + "cleaned_test.txt"));
			BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream(fileDirs), "UTF-8"));
			
			while( (text = in.readLine()) != null ){
				if(text.isEmpty() || text.equals("")){
					continue;
				}
				try {
					 
					HashMap<String, Integer> dependencies = sentenceDep(text);
					
					for(String key : depens){
							features.put(key, features.get(key) + dependencies.get(key));
					}
				} catch (Exception e) {
					//e.printStackTrace();
					continue;
				}
			}
			in.close();
			
			PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(new FileOutputStream(PATH + "depen_" + filename), "UTF-8")));

			for(String key : features.keySet()){
				out.println(key + " " + features.get(key).toString());
			}
			out.close();
			
			out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(new FileOutputStream(PATH + "depen_text_" + filename), "UTF-8")));
			out.print(saveText);
			out.close();
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	
	public static void main(String[] args) { 
		// TODO Auto-generated method stub
		//String[] files = split(args[0]);
		String[] files = split("luxun.txt");
		for(String file : files){
			run(file);
		}
		
		System.out.println("Java Program Finished!");
	}

}
