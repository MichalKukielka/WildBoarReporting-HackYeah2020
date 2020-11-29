import React, {useContext} from 'react';
import {View, StyleSheet} from 'react-native';
import {AuthContext} from '../navigation/AuthProvider';
import FormButton from '../components/FormButton';

const HomeScreen = () => {
  const {logout} = useContext(AuthContext);

  return (
    <View style={styles.container}>
      <FormButton buttonTitle="Sign Out from Home" onPress={() => logout()} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#f9fafd',
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  logo: {
    height: 150,
    width: 150,
    resizeMode: 'cover',
  },
  text: {
    fontSize: 28,
    marginBottom: 10,
  },
  navButton: {
    marginTop: 15,
  },
  forgotButton: {
    marginVertical: 35,
  },
  navButtonText: {
    fontSize: 18,
    fontWeight: '500',
    color: '#2e64e5',
  },
});

export default HomeScreen;
