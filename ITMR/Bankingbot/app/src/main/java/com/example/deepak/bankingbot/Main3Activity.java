package com.example.deepak.bankingbot;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;


public class Main3Activity extends AppCompatActivity {
    JSONObject jsonObject;
    EditText a;
    EditText password;
    EditText account_branch;
    EditText sex;
    EditText p;
    EditText s;
    Button submit;
    String postjson="";
    String url;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.signup2);
        submit=(Button)findViewById(R.id.button3);

        Intent intent=getIntent();
        String f_name=intent.getStringExtra("f_name");
        String l_name=intent.getStringExtra("l_name");
        String email=intent.getStringExtra("email");
        String Age=intent.getStringExtra("Age");
        String Adress=intent.getStringExtra("Adress");
        String p_no=intent.getStringExtra("p_no").trim();
        int age=Integer.parseInt(Age);
        int phone_no=Integer.parseInt(p_no);
         password=(EditText)findViewById(R.id.editText10);
         account_branch=(EditText)findViewById(R.id.editText14);
         sex=(EditText)findViewById(R.id.editText13);

        try {
System.out.println(sex.getText().toString());
            System.out.println(account_branch.getText().toString());
             jsonObject = new JSONObject();
            jsonObject.put("first_name", f_name);
            jsonObject.put("last_name",l_name);
            jsonObject.put("email",email);
            jsonObject.put("age",age);
            jsonObject.put("address",Adress);
            jsonObject.put("phone_number",phone_no);
            jsonObject.put("user_name",email);
            jsonObject.put("account_balance",Integer.parseInt("10000"));


            url="http://10.0.2.2:4666/api/create_customer_info";

        }catch (Exception exception){

            exception.printStackTrace();
        }


    }
public void submit(View view){
    try{jsonObject.put("account_branch",account_branch.getText().toString());
    jsonObject.put("sex",sex.getText().toString());
    jsonObject.put("password",password.getText().toString());
        postjson=jsonObject.toString();

    }catch (Exception e){e.printStackTrace();}
   final String requestBody=postjson;
    RequestQueue requestQueue= Volley.newRequestQueue(this);
    StringRequest stringRequest = new StringRequest(Request.Method.POST, url, new Response.Listener<String>() {
        @Override
        public void onResponse(String response) {
        System.out.println(response);
        }
    }, new Response.ErrorListener() {
        @Override
        public void onErrorResponse(VolleyError error) {

        }
    }) {
        @Override
        public String getBodyContentType() {
            return String.format("application/json; charset=utf-8");
        }

        @Override
        public byte[] getBody() throws AuthFailureError {
            try {
                return requestBody == null ? null : requestBody.getBytes("utf-8");
            } catch (Exception uee) {
                VolleyLog.wtf("Unsupported Encoding while trying to get the bytes of %s using %s",
                        requestBody, "utf-8");
                return null;
            }
        }
    };
    requestQueue.add(stringRequest);
}


}


