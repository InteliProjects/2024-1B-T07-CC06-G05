import unittest
import pandas as pd
import data_processing as dp
from io import StringIO
from custom_exceptions.custom_exception import CustomException


class TestCsvDataProcessing(unittest.TestCase):

    def setUp(self):
        self.data = StringIO("INDICE;LATITUDE;LONGITUDE;CODIGO_ROTA;SEQUENCIA;LOGRADOURO;NUMERO\n"
                                "1;45.0;45.0;001;1;Main Street;100")
        self.processed_data = StringIO("INDICE,LATITUDE,LONGITUDE,LOGRADOURO,NUMERO\n"
                                          "1,45.0,45.0,Main Street,100")
        self.bad_data = StringIO("BAD_HEADER\n"
                                    "bad_data")
        self.empty_data = StringIO("")
        
    def test_write_to_tmp_file(self):
        filename = dp.write_to_tmp_file(self.data)
        self.assertIn(filename, dp.generated_files) 

    def test_remove_generated_files(self):
        dp.write_to_tmp_file(self.data) 
        dp.remove_generated_files()
        self.assertEqual(len(dp.generated_files), 0)  

    def test_prepare_initial_data(self):
        result = dp.prepare_initial_data(self.data)
        result.seek(0)
        self.assertEqual(result.read(), self.processed_data.getvalue())

    def test_prepare_algorithm_data(self):
        result = dp.prepare_algorithm_data(self.data)
        result.seek(0)
        self.assertIn("LOGRADOURO", result.read())

    def test_merge_data(self):
        initial_data = dp.prepare_initial_data(self.data)
        algorithm_response = dp.prepare_algorithm_data(self.data)
        final_data = dp.merge_data(initial_data, algorithm_response)
        final_data.seek(0)
        self.assertIn("LOGRADOURO", final_data.read())

    def test_IO_as_dataframe(self):
        df = dp._IO_as_dataframe(self.data)
        self.assertFalse(dp._is_invalid_format(df))

    def test_is_invalid_format(self):
        df = dp._IO_as_dataframe(self.data)
        self.assertFalse(dp._is_invalid_format(df))

    def test_df_to_IO(self):
        df = dp._IO_as_dataframe(self.data)
        result = dp._df_to_IO(df, "test.csv")
        result.seek(0)
        self.assertIn("Main Street", result.read())

    def test_common_pipeline(self):
        df = dp._IO_as_dataframe(self.data)
        dp._common_pipeline(df)
        self.assertNotIn("CODIGO_ROTA", df.columns)

    def test_drop_unnecessary_cols(self):
        df = dp._IO_as_dataframe(self.data)
        dp._drop_unnecessary_cols(df)
        self.assertNotIn("CODIGO_ROTA", df.columns)

    def test_fill_null_vals(self):
        df = pd.DataFrame({
            "NUMERO": [None, "123", None],
            "LOGRADOURO": ["Elm Street", "Pine Avenue", "Maple Avenue"]
        })
        dp._fill_null_vals(df)
        self.assertEqual(df.loc[0, "NUMERO"], 0)

    def test_clean_number_column(self):
        df = pd.DataFrame({
            "NUMERO": ["100a", "200", "Three"]
        })
        dp._clean_number_column(df)
        self.assertEqual(df.loc[0, "NUMERO"], '100')
        self.assertEqual(df.loc[2, "NUMERO"], '0')

    def test_convert_float_cols_to_int(self):
        df = pd.DataFrame({
            "NUMERO": [1.0, 2.0],
            "INDICE": [1.0, 2.0]
        })
        dp._convert_float_cols_to_int(df)
        self.assertTrue(pd.api.types.is_integer_dtype(df['NUMERO']))

    def test_drop_coordinates_cols(self):
        df = dp._IO_as_dataframe(self.data)
        dp._drop_coordinates_cols(df)
        self.assertNotIn("LATITUDE", df.columns)

    def test_drop_indice_col(self):
        df = dp._IO_as_dataframe(self.data)
        dp._drop_indice_col(df)
        self.assertNotIn("INDICE", df.columns)

    def test_add_hydrometer_count_col(self):
        df = pd.DataFrame({
            "LOGRADOURO": ["Elm Street", "Elm Street", "Pine Avenue", "Maple Avenue"],
            "NUMERO": ["100", "100", "200", "300"]
        })
        df = dp._add_hydrometer_count_col(df)
        self.assertIn("QUANTIDADE_HIDROMETROS", df.columns)

    def test_get_adress_number(self):
        result = dp._get_adress_number("123B")
        self.assertEqual(result, '123')

    def test_get_number_within_str(self):
        result = dp._get_number_within_str("Apartment 30")
        self.assertEqual(result, '30')

    def test_errors(self):
        with self.assertRaises(CustomException):
            dp._IO_as_dataframe(self.bad_data) 

        with self.assertRaises(CustomException):
            df = dp._IO_as_dataframe(self.data)
            dp._drop_coordinates_cols(df)  

    def test_IO_as_dataframe_invalid(self):
        with self.assertRaises(Exception):
            dp._IO_as_dataframe(self.empty_data)

    def test_initial_data_pipeline_exception(self):
        with self.assertRaises(Exception):
            dp.prepare_initial_data(self.bad_data)

    def test_algorithm_data_pipeline_exception(self):
        with self.assertRaises(Exception):
            dp.prepare_algorithm_data(self.bad_data)

if __name__ == '__main__':
    unittest.main()
