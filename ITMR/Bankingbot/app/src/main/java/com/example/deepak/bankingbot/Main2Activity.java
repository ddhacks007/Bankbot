package com.example.deepak.bankingbot;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.EditText;

public class Main2Activity extends AppCompatActivity {
EditText f_name;
    EditText l_name;
    EditText email;
    EditText Age;
    EditText Adress;
    EditText p_no;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.signup);
f_name=(EditText)findViewById(R.id.editText);
        l_name=(EditText)findViewById(R.id.editText2);
        email=(EditText)findViewById(R.id.editText3);
        Age=(EditText)findViewById(R.id.editText4);
        Adress=(EditText)findViewById(R.id.editText5);
        p_no=(EditText)findViewById(R.id.editText6);

    }
    public  void nextActivity(View view){

        Intent intent=new Intent(this,Main3Activity.class);
        intent.putExtra("f_name",f_name.getText().toString());
        intent.putExtra("l_name",l_name.getText().toString());
        intent.putExtra("email",email.getText().toString());
        intent.putExtra("Age",Age.getText().toString());
        intent.putExtra("Adress",Adress.getText().toString());
        intent.putExtra("p_no",p_no.getText().toString());
        startActivity(intent);


    }
}