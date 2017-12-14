
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import org.fnlp.nlp.cn.CNFactory;
import org.fnlp.nlp.parser.dep.DependencyTree;
import org.fnlp.util.exception.LoadModelException;

public class Test {

	// 30 dependency features
	public final static String[] depens = { "之字结构", "时态", "构式", "修饰", "话题", "关联", "同位", "数量", "顺承", "定语", "主语", "限定",
			"从属", "介宾", "标签", "连动", "总括", "标点", "的字结构", "Root", "宾语", "语态", "并列", "得字结构", "地字结构", "核心词", "疑问连动", "感叹",
			"补语", "状语" };
	public static final String PATH = "..\\src\\output\\";

	private static String saveText = new String();
	private static HashMap<String, Integer> prime = new HashMap<String, Integer>();

	public static String makeText() {
		return saveText;
	}

	public static HashMap<String, Integer> computeDepen(ArrayList<java.util.List<String>> result) {
		HashMap<String, Integer> grammar_counter = new HashMap<String, Integer>();

		for (String item : depens) {
			grammar_counter.put(item, 0);
		}
		List<String> tmp;
		String newText = new String();

		for (int i = 0; i < result.size(); i++) {
			tmp = result.get(i);
			String grammar_tag = tmp.get(3);
			newText += Arrays.asList(depens).indexOf(grammar_tag) + " ";
			// System.out.println(tmp.toString());
			grammar_counter.put(grammar_tag, grammar_counter.get(grammar_tag) + 1);

		}
		// Accumulate all the sentences
		saveText += newText + "\n";
		return grammar_counter;
	}

	public static HashMap<String, Integer> sentenceDep(String sentence) throws LoadModelException {

		CNFactory factory = CNFactory.getInstance("models");
		DependencyTree tree = factory.parse2T(sentence);
		ArrayList<java.util.List<String>> result = tree.toList();

		return computeDepen(result);
	}

	public static String[] split(String filenames) {
		return filenames.split(",");
	}

	public static HashMap<String, Integer> extractFeatures(String file) throws IOException {
		// Initialize features hash map
		HashMap<String, Integer> features = new HashMap<String, Integer>();
		for (String item : depens) {
			features.put(item, 0);
		}

		File fileDirs = new File(PATH + file);
		String text;
		BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream(fileDirs), "UTF-8"));

		while ((text = in.readLine()) != null) {
			if (text.isEmpty() || text.equals("") || text.equals("\n")) {
				continue;
			}
			try {
				HashMap<String, Integer> dependencies = sentenceDep(text);
				for (String key : depens) {
					features.put(key, features.get(key) + dependencies.get(key));
				}
			} catch (Exception e) {
				e.printStackTrace();
				continue;
			}
		}
		in.close();
		return features;
	}

	public static void saveFeatures(String author, HashMap<String, Integer> features)
			throws UnsupportedEncodingException, FileNotFoundException {
		PrintWriter out = new PrintWriter(new BufferedWriter(
				new OutputStreamWriter(new FileOutputStream(PATH + "depen_" + author + ".txt"), "UTF-8")));

		for (String key : features.keySet()) {
			out.println(key + " " + features.get(key).toString());
		}
		out.close();
	}

	public static void saveEncodedText(String author) throws UnsupportedEncodingException, FileNotFoundException {
		PrintWriter out = new PrintWriter(new BufferedWriter(
				new OutputStreamWriter(new FileOutputStream(PATH + "depen_text_" + author + ".txt"), "UTF-8")));
		out.print(saveText);
		out.close();
	}

	public static void encodeAuthor(String filename, String author) {
		try {
			// Compute all sentence dependency features of a single file
			HashMap<String, Integer> features = extractFeatures(filename);
			saveFeatures(author, features);
			saveEncodedText(author);

		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public static ArrayList<String> getPrime() {
		BufferedReader in;
		ArrayList<String> authors = new ArrayList<String>();
		try {
			in = new BufferedReader(new InputStreamReader(new FileInputStream("..\\src\\output\\prime.txt"), "UTF-8"));
			String line;

			while ((line = in.readLine()) != null) {
				String[] strings = line.split(" ");
				String author_name = strings[0];
				prime.put(author_name, Integer.parseInt(strings[1]));
				authors.add(author_name);
			}
			in.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return authors;
	}
	
	public static void encodeSingleFile(String filename, String author){
		HashMap<String, Integer> features;
		try {
			features = extractFeatures(filename);
			System.out.println(features.toString());
			saveFeatures(author, features);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		ArrayList<String> authorList = getPrime();
		for (String author : authorList) {

			//System.out.println("dealing with cleaned_" + author + ".txt ...");
			//encodeAuthor("cleaned_" + author + ".txt", author);
			
			for (Integer cnt = 0; cnt < prime.get(author); cnt++) {
				
				System.out.println("dealing with cleaned_" + author + cnt.toString() + ".txt...");
				encodeSingleFile("cleaned_" + author + cnt.toString() + ".txt", author + cnt.toString());
			}
		}

		System.out.println("Java Program Finished!");
	}

}
